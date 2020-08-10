"""
This file houses the unit test suite for viewing the goal customization interface
of a restaurant profile.
"""
import os
import sys
import pytest
from bson.objectid import ObjectId

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

def test_custom_goals_route_no_login(client):
    """
    Test that goal customization page does not load unless user is logged in.
    """
    res = client.get("/customize", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_custom_goals_route_logged_in(client):
    """
    Test that goal customization page loads when the user is logged in.
    """
    client.post("/login", data={"username": "janedoe", "password": "Aa123456"})
    res = client.get("/customize", follow_redirects=True)
    assert b"Customization" in res.data

def test_add_goal_not_logged_in(client):
    """
    Test that a user cannot add a goal when they're not logged in.
    """
    res = client.post("/customize/add-goal", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_delete_goal_not_logged_in(client):
    """
    Test that a user cannot delete a goal when they're not logged in.
    """
    some_id = {"deleted-goal": "5f11c9721a52881b3573c029"} # Utilize an actual existing ID.
    res = client.post("/customize/delete-goal", data=some_id, follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_get_custom_goals():
    """
    Test that get_custom_goals() function in restaurant_profile_manager.py
    retrieves the correct list of custom goals of a restaurant profile.
    """
    rpm = RestaurantProfileManager("janedoe")
    gm = GoalsManager(rpm)
    custom_goals = gm.get_custom_goals()
    expected_custom_goals = [{
        '_id': ObjectId("5f11c9721a52881b3573c029"),
        'goal': "This is a custom goal."
    }, {
        '_id': ObjectId("5f11c99a1a52881b3573c02a"),
        'goal': "This is another custom goal."
    }]
    assert custom_goals == expected_custom_goals
