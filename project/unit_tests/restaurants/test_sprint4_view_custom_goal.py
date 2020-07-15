"""
This file houses the unit test suite for viewing the goal customization interface
of a restaurant profile.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from bson.objectid import ObjectId
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

def test_custom_goals_route_logged_in(client):
    """
    Test that restauarant view restaurant profile page loads when the user is logged in.
    """
    client.post("/login", data={"username": "janedoe", "password": "Aa123456"})
    res = client.get("/custom-goals", follow_redirects=True)
    assert b"Edit Profile" in res.data

def test_get_custom_goals():
    """
    Test that get_custom_goals() function in restaurant_profile_manager.py
    retrieves the correct list of custom goals of a restaurant profile.
    """
    rpm = RestaurantProfileManager("janedoe")
    custom_goals = rpm.get_custom_goals()
    expected_custom_goals = [{
        '_id': ObjectId("5f0f4a09647ec38058dc4446"),
        'goal': "This is my custom goal."
    }, {
        '_id': ObjectId("5f0f4a79647ec38058dc4447"),
        'goal': "This is another custom goal."
    }]
    assert custom_goals == expected_custom_goals
