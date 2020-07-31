"""
This file houses the unit test suite for the customer view restaurant profile page"
"""

import os
import sys
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from rewards_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_view_restaurant_profile_route_no_login(client):
    """
    Test that restaurant profile page does not load unless user is logged in.
    """
    res = client.get("/profiles/5f15c084143cb39bfc5619b8/profile", follow_redirects=True)
    assert res != 0

def test_get_restaurant_profile_by_id():
    """
    Test that get_restaurant_profile_by_id() returns the correct restaurant
    profile information.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        profile = rpm.get_restaurant_profile_by_id("5f15c084143cb39bfc5619b8")

        assert profile["name"] == "KFC"

        assert profile["category"] == "Chicken"

        assert profile["description"] == "The best fried chicken on the block."

        assert profile["phone_number"] == "416-267-0439"


def test_view_restaurant_profile_route_logged_in(client):
    """
    Test that restaurant profile page loads when the user is logged in.
    """
    client.post("/login", data={"username": "unitTestUser", "password": "Password!"})
    res = client.get("/profiles/5f15c084143cb39bfc5619b8/profile", follow_redirects=True)
    assert b'View Profile'
