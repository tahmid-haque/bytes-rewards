"""
This file houses the unit test suite for adding custom goals to a board.
"""

import os
import sys
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from restaurants_app import app
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.goals import GoalsManager

@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_view_board_route_no_login(client):
    """
    Test that view board page does not load unless user is logged in.
    """
    res = client.get("/", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_save_board_route_no_login(client):
    """
    Test that a user is unable to save a board unless they are logged in.
    """
    res = client.post("/save", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data


def test_view_board_route_logged_in(client):
    """
    Test that edit view board page loads when the user is logged in.
    """
    client.post("/login",
                data={
                    "username": "unittestuser",
                    "password": "Jake1234"
                })
    res = client.get("/", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data


def test_save_board_route_logged_in(client):
    """
    Test that a user is able to save a board when they are logged in.
    """
    client.post("/login",
                data={
                    "username": "unittestuser",
                    "password": "Jake1234"
                })
    res = client.post(
        "/save",
        follow_redirects=True)

    assert b"Please log in to access this page" not in res.data


def test_get_custom_goals():
    """
    Test that the get_custom_goals() function in restaurant_profile_manager.py retrieves the user's custom goals
    """
    rpm = RestaurantProfileManager("unittestuser")
    gm = GoalsManager(rpm)
    goals = gm.get_custom_goals()
    assert len(goals) == 2

def test_get_goals():
    """
    Test that the get_goals() function in restaurant_profile_manager.py retrieves all the user's goals, there are
    20 shared goals, then anything extra will custom goals
    """
    rpm = RestaurantProfileManager("vchang")
    gm = GoalsManager(rpm)
    goals = gm.get_goals()
    assert len(goals) >= 20


