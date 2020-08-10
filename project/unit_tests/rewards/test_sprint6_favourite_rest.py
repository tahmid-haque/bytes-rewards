"""
This file houses the unit test suite favourite feature and interface
 on the rewards app.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from bson.objectid import ObjectId
from rewards_app import app
from modules.owner.public_profile import PublicProfileModifier
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.customer.customer_profile_manager import CustomerProfileManager
from modules.customer.favourite import *
from modules.customer.customer_board import *


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_get_favourites():
    """
    Test that get_favourite() returns a list of restaurant ids.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        cpm = CustomerProfileManager("ksawyer")
        favourite = get_favourite(cpm)
        assert len(favourite) > 0


def test_get_no_favourite():
    """
    Test that get_favourite() returns an empty list of restaurant ids
    if user has no favourites.
    """
    with app.app_context():
        cpm = CustomerProfileManager("unittestuser")
        favourite = get_favourite(cpm)
        assert len(favourite) == 0


def test_update_favourite():
    """
    Test that update_favourite() updates the user's list of favourite
    restaurant Ids.
    """
    with app.app_context():
        cpm = CustomerProfileManager("ksawyer")
        old_favourite = get_favourite(cpm)
        if ObjectId('5f15c084143cb39bfc5619b8') in old_favourite:
            expected = len(old_favourite) - 1
        else:
            expected = len(old_favourite) + 1
        new_favourite = update_favourite(cpm, '5f15c084143cb39bfc5619b8')
    assert len(new_favourite) == expected

def test_get_favourite_doc():
    """
    Test that get_favourite_doc() returns a dictionary of favourite
    restaurant profiles.
    """
    with app.app_context():
        cpm = CustomerProfileManager("testuser")
        rpm = RestaurantProfileManager("")
        ppm = PublicProfileModifier(rpm)
        all_profiles = ppm.get_public_profiles()
        favourite = get_favourite(cpm)
        profiles = get_favourite_doc(all_profiles, favourite)
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

def test_favourite_not_logged_in(client):
    """
    Test that a user cannot favourite a restaurant when they're not logged in.
    """
    restaurant = {"restaurant-id": "5f15c084143cb39bfc5619b8"} # Utilize an actual existing ID.
    res = client.post("/personal/favourites", data=restaurant, follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_view_favourites_not_logged_in(client):
    """
    Test that user cannot view favourite restaurants when they're not logged in.
    """
    res = client.post("/personal/favourites", follow_redirects=True)
    assert b"Please log in to access this page" in res.data

def test_view_and_favourite_not_logged_in(client):
    """
    Test that a user cannot favourite a restaurant when they're not logged in.
    """
    restaurant = {"restaurant-id": "5f15c084143cb39bfc5619b8"} # Utilize an actual existing ID.
    res = client.post("/personal/favourites", 
                      data=restaurant, follow_redirects=True)
    assert b"Please log in to access this page" in res.data
