from bson.objectid import ObjectId
"""
This file houses the unit test suite for adding a custom goal to a restaurant profile.
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

def test_add_custom_goal():
    """
    Test that add_custom_goal() function in restaurant_profile_manager.py
    adds a custom goal to the restaurant profile, given that it is not in 
    the database.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        existing_goal_dict = rpm.get_custom_goals()
        existing_goal_list = [x['goal'] for x in existing_goal_dict]
        count = 2
        inList = True
        while inList:
            expected_goal = "Buy " + str(count) + " desserts in one visit"
            count += 1
            if expected_goal not in existing_goal_list:
                inList = False
        rpm.add_custom_goal(expected_goal)
        goal_list = rpm.get_custom_goals()
        
        goal = [x for x in goal_list if x['goal'] == expected_goal]
        
        assert (expected_goal in goal[0]['goal'])


def test_add__duplicate_custom_goal():
    """
    Test that add_custom_goal() function in restaurant_profile_manager.py
    does not add a custom goal to the restaurant profile, given that it is in 
    the database.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        existing_goal_dict = rpm.get_custom_goals()
        existing_goal_list = [x['goal'] for x in existing_goal_dict]
        dupe_goal = existing_goal_list[0]
        rpm.add_custom_goal(dupe_goal)
        goal_list = rpm.get_custom_goals()
        
        goal = [x for x in goal_list if x['goal'] == dupe_goal]
        
        assert len(goal) == 1

def test_get_custom_goals():
    """
    Test that get_custom_goals function in restaurant_profile_manager.py
    returns the user's list of custom goals.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        goals = rpm.get_custom_goals()
        hasFields = True
        for goal in goals:
            if goal['_id'] == None and goal['goal'] == None:
                hasFields = False
        
        assert len(goals) > 0 and hasFields
    