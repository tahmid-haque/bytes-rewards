"""
This file houses the unit test suite for adding a custom reward to a restaurant profile.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from restaurants_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager


def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    return app


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_add_custom_reward():
    """
    Test that add_custom_reward() function in restaurant_profile_manager.py
    adds a custom reward to the restaurant profile, given that it is not in
    the database.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        existing_reward_dict = rpm.get_rewards()
        existing_reward_list = [x['reward'] for x in existing_reward_dict]
        count = 2
        in_list = True
        while in_list:
            expected_reward = "Get " + str(
                count) + " free desserts in one visit"
            count += 1
            if expected_reward not in existing_reward_list:
                in_list = False
        rpm.add_custom_reward(expected_reward)
        reward_list = rpm.get_rewards()

        reward = [x for x in reward_list if x['reward'] == expected_reward]

        assert expected_reward in reward[0]['reward']


def test_add__duplicate_custom_reward():
    """
    Test that add_custom_reward() function in restaurant_profile_manager.py
    does not add a custom reward to the restaurant profile, given that it is in
    the database.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        existing_reward_dict = rpm.get_rewards()
        existing_reward_list = [x['reward'] for x in existing_reward_dict]
        dupe_reward = existing_reward_list[0]
        rpm.add_custom_reward(dupe_reward)
        reward_list = rpm.get_rewards()

        reward = [x for x in reward_list if x['reward'] == dupe_reward]

        assert len(reward) == 1


def test_get_custom_rewards():
    """
    Test that get_custom_rewards function in restaurant_profile_manager.py
    returns the user's list of custom rewards.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        rewards = rpm.get_custom_rewards()
        has_fields = True
        for reward in rewards:
            if reward['_id'] is None and reward['reward'] is None:
                has_fields = False

        assert len(rewards) >= 0 and has_fields
