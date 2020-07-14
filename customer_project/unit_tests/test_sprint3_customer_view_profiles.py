"""
This file houses the unit test suite for the customer view restaurant profile page"
"""


import os
import sys
import pytest
from bson.objectid import ObjectId
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '../src'))   # Import the src folder


from app import app
from customer_profile_manager import CustomerProfileManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_edit_profile_route_logged_in(client):
    """
    Test that customer view restaurant profile page loads when the user is logged in.
    """
    client.post("/customer_login",
                data={
                    "username": "unitTestUser",
                    "password": "Password!"
                })
    res = client.get("/view_profiles", follow_redirects=True)
    assert b"Choose a Game Board" in res.data


def test_get_restaurant_profiles():
    """
    Test that get_restaurant_profiles() function in customer_profile_manager.py retreives all
    restaurant profile fields that are public.
    """
    rpm = CustomerProfileManager(app, "unitTestUser")
    profiles = rpm.get_restaurant_profiles()
    expected_fields = ["name", "category", "image", "is_public"]
    
    has_id = True
    has_fields = True
    is_public = True
    for key in list(profiles.keys()):
        if type(key) != ObjectId:
            has_id = False
            break
        fields = list(profiles[key].keys())
        for f in expected_fields:
            if f not in fields:
                has_fields = False
                break
        if profiles[key]["is_public"] == False:
            is_public = False
            break
        
    assert len(profiles) > 0 and has_id and has_fields and is_public
