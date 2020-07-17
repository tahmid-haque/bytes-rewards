"""
This file houses the unit test suite for the edit restaurant profile feature.
"""

import os
import sys
import pytest
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

def test_remove_custom_goal():
    """
    Test that the remove_custom_goal() function in 
    restaurant_profile_manager.py can be used to remove
    a user's custom goal.
    """
    rpm = RestaurantProfileManager("vchang")
    old_goals = rpm.get_custom_goals()
    rpm.remove_custom_goal(old_goals[0]['_id'])
    new_goals = rpm.get_custom_goals()
    assert len(new_goals) < len(old_goals)

