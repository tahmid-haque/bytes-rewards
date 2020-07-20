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
from modules.restaurant_profile_manager import RestaurantProfileManager

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
    res = client.get("/goals", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_custom_goals_route_logged_in(client):
    """
    Test that goal customization page loads when the user is logged in.
    """
    client.post("/login", data={"username": "janedoe", "password": "Aa123456"})
    res = client.get("/goals", follow_redirects=True)
    assert b"Customization" in res.data

def test_add_goal_not_logged_in(client):
    """
    Test that a user cannot add a goal when they're not logged in.
    """
    res = client.post("/goals/add", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_delete_goal_not_logged_in(client):
    """
    Test that a user cannot delete a goal when they're not logged in.
    """
    some_id = "5f11c9721a52881b3573c029" # Utilize an actual existing ID.
    res = client.post("/goals/"+some_id+"/delete", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_get_custom_goals():
    """
    Test that get_custom_goals() function in restaurant_profile_manager.py
    retrieves the correct list of custom goals of a restaurant profile.
    """
    rpm = RestaurantProfileManager("janedoe")
    custom_goals = rpm.get_custom_goals()
    expected_custom_goals = [{
        'id': ObjectId("5f11c9721a52881b3573c029"),
        'goal': "This is a custom goal."
    }, {
        'id': ObjectId("5f11c99a1a52881b3573c02a"),
        'goal': "This is another custom goal."
    }]
    assert custom_goals == expected_custom_goals
