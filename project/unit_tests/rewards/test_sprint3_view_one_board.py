"""
This file houses the unit test suite for the edit restaurant profile feature.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from rewards_app import app
from modules.customer_profile_manager import CustomerProfileManager
from modules.restaurant_profile_manager import RestaurantProfileManager


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
    res = client.get("/profiles/objid/board", follow_redirects=True)
    assert res != 0


def test_get_goals():
    """
    Test that the get_goals() function in customer_profile_manager.py retrieves all
    all restaurant goal ids.
    """
    with app.app_context():
        user = CustomerProfileManager("vchang")
        goals = user.get_goals()
    assert len(goals) != 0


def test_get_rewards():
    """
    Test that the get_rewards() function in customer_profile_manager.py retrieves all
    all restaurant reward ids.
    """
    with app.app_context():
        user = CustomerProfileManager("vchang")
        rewards = user.get_rewards()
    assert len(rewards) != 0


def test_get_restaurant_users():
    """
    Test that the get_restaurant_users() function in customer_profile_manager.py retrieves all
    all restaurant users.
    """
    with app.app_context():
        user = RestaurantProfileManager("vchang")
        users = user.get_public_users()
    assert len(users) != 0


def test_view_board_route_logged_in(client):
    """
    Test that edit profile page loads when the user is logged in.
    """
    client.post("/login", data={"username": "junaid", "password": "Junaid123"})
    res = client.get("/profiles/objid/board", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data
