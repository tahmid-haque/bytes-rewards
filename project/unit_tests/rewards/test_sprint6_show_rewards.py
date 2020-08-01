"""
This file houses the unit test suite for the show rewards interface on the rewards app.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from rewards_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager
from modules.customer_profile_manager import CustomerProfileManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_get_restaurant_name_by_id_valid():
    """
    Test that get_restaurant_name_by_id() returns the restaurant name of a valid user correctly.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        username = rpm.get_restaurant_name_by_id("5f15c084143cb39bfc5619b8")
        assert username == "KFC"


def test_get_restaurant_name_by_id_invalid():
    """
    Test that get_restaurant_name_by_id() returns "" for invalid ids.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        username = rpm.get_restaurant_name_by_id("not a real id")
        assert username == ""


def test_get_reward_progress_empty():
    """
    Test that get_reward_progress() returns empty data for users with no reward progress.
    """
    with app.app_context():
        cpm = CustomerProfileManager("newuser")
        assert cpm.get_reward_progress() == ([], [])


def test_get_reward_progress_non_empty():
    """
    Test that get_reward_progress() returns correct data for users with reward progress.
    """
    with app.app_context():
        cpm = CustomerProfileManager("showrewardsuser")
        expected_progress = ([{
            'is_redeemed': False,
            'redemption_code': '4209cf81f02e409690930032ed771465',
            'restaurant_name': 'KFC',
            'text': 'One Free Drink Refill'
        }, {
            'is_redeemed': False,
            'redemption_code': '43adf2823896a666d8000fb5ffea7666',
            'restaurant_name': 'KFC',
            'text': '15% Off A Purchase'
        }, {
            'is_redeemed': False,
            'redemption_code': '06e9ac1d92cbfad29f55a3efee01bd41',
            'restaurant_name': 'Too Good To Be True',
            'text': '$3 Off Any Entree'
        }], [{
            'is_redeemed': True,
            'redemption_code': '14991fd515dbd032152e59d9db6bd4b5',
            'redemption_date': 'July 28, 2020',
            'restaurant_name': 'KFC',
            'text': '$10 Off Any $50+ Purchase'
        }, {
            'is_redeemed': True,
            'redemption_code': '54a3c1b86dfbfa0cc00cf1c7c7e8d211',
            'redemption_date': 'May 20, 2018',
            'restaurant_name': 'KFC',
            'text': 'Free Dessert'
        }, {
            'is_redeemed': True,
            'redemption_code': '43adf2823896a666d8000fb5ffea7666',
            'redemption_date': 'July 11, 2006',
            'restaurant_name': 'KFC',
            'text': '10% Off A Purchase'
        }])
        assert cpm.get_reward_progress() == expected_progress


def test_show_rewards_not_logged_in(client):
    """
    Test that the show rewards interface does not appear when users are not logged in.
    """
    res = client.get("/personal/rewards", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_show_rewards_qr_code(client):
    """
    Test that the shwo rewards interface contains the correct QR code for each active reward.
    """
    client.post("/login",
                data={
                    "username": "showrewardsuser",
                    "password": "Password!"
                })
    res = client.get("/personal/rewards", follow_redirects=True)

    progress = CustomerProfileManager("showrewardsuser").get_reward_progress()

    for reward in progress[0]:
        assert str.encode(reward["redemption_code"]) in res.data
