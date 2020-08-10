"""
This file houses the unit test suite for Scanning qr codes for customer goals and
makring the goals as complete
"""
import os
import sys
import pytest
from bson.objectid import ObjectId

sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from restaurants_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.rewards import RewardsManager

@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()

def test_valid_completed_reward(client):
    """
    Test that a user can mark a valid reward as complete.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("junaid")
        rm = RewardsManager(rpm)
        code = "junaid+5f03a9fd7aae4a086d810102+6".split("+")
        msg = rm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+6")
        assert msg == "Code has already been redeemed!"

def test_duplicate_completed_reward(client):
    """
    Test that a duplicate reward can't be completed again.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("junaid")
        rm = RewardsManager(rpm)
        code = "junaid+5f03a9fd7aae4a086d810102+6".split("+")
        msg = rm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+6")
        assert msg == "Code has already been redeemed!"

def test_invalid_reward(client):
    """
    Test that a user can't complete an invalid reward.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("junaid")
        rm = RewardsManager(rpm)
        code = "junaid+5f03a9fd7aae4a086d810102+7".split("+")
        msg = rm.complete_reward(code[0], "junaid+5f03a9fd7aae4a086d810102+7")
        assert msg == "Invalid QR code!"
