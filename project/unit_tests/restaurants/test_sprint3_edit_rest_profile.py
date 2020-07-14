"""
This file houses the unit test suite for the edit restaurant profile feature.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../src'))  # Import the src folder

from restaurants_app import app
from restaurant_profile_manager import RestaurantProfileManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_edit_profile_route_no_login(client):
    """
    Test that edit profile page does not load unless user is logged in.
    """
    res = client.get("/profile/edit", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_edit_profile_route_logged_in(client):
    """
    Test that edit profile page loads when the user is logged in.
    """
    client.post("/login",
                data={
                    "username": "unittestuser",
                    "password": "Jake1234"
                })
    res = client.get("/profile/edit", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data
    assert b"Edit Profile" in res.data


def test_save_profile_route_no_login(client):
    """
    Test that a user is unable to save a profile unless they are logged in.
    """
    res = client.post("/profile/save", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_save_profile_route_logged_in(client):
    """
    Test that a user is able to save a profile when they are logged in.
    """
    client.post("/login",
                data={
                    "username": "unittestuser",
                    "password": "Jake1234"
                })
    res = client.post(
        "/profile/save",
        follow_redirects=True,
        data={
            "name":
                "Jake's",
            "category":
                "BBQ",
            "image":
                "https://restaurantengine.com/wp-content/uploads/2015/05/startup-restaurants-typically-overspend.jpg",
            "description":
                "It's a pretty good bbq place.",
            "phone_number":
                "4166543785",
            "is_public":
                "on",
            "location[address]":
                "1265 Military Trail",
            "location[postal_code]":
                "M1C1A4",
            "location[city]":
                "Scarborough",
            "location[province]":
                "ON"
        })
    assert b"Please log in to access this page" not in res.data


def test_get_profile_new_user():
    """
    Test that the get_profile() function in restaurant_profile_manager.py retrieves an
    empty profile when a new user is detected.
    """
    rpm = RestaurantProfileManager(app, "newuser")
    profile = rpm.get_profile()
    assert profile == {}


def test_get_profile_old_user():
    """
    Test that the get_profile() function in restaurant_profile_manager.py retrieves a user's
    profile given that they have set up their profile before.
    """
    rpm = RestaurantProfileManager(app, "unittestuser")
    profile = rpm.get_profile()
    expected_profile = {
        "name":
            "Jake's",
        "category":
            "BBQ",
        "image":
            "https://restaurantengine.com/wp-content/uploads/2015/05/startup-restaurants-typically-overspend.jpg",
        "description":
            "It's a pretty good bbq place.",
        "phone_number":
            "4166543785",
        "is_public":
            True,
        "location": {
            "address": "1265 Military Trail",
            "postal_code": "M1C1A4",
            "city": "Scarborough",
            "province": "ON"
        }
    }
    assert profile == expected_profile


def test_update_profile():
    """
    Test that the update_profile() function in restaurant_profile_manager.py can be used to update
    a user's profile to the given profile.
    """
    rpm = RestaurantProfileManager(app, "unittestuser")
    old_profile = rpm.get_profile()

    new_profile = old_profile.copy()
    new_profile["name"] = old_profile["name"] + "edited"
    rpm.update_profile(new_profile)

    assert rpm.get_profile() == new_profile

    rpm.update_profile(old_profile)
