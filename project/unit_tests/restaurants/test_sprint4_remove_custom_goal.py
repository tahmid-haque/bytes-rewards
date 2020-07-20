"""
This file houses the unit test for remoce custom goal backend.
"""

import os
import sys
import pytest
import random 
from random import randint
from bson.objectid import ObjectId
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
	
def test_remove_custom_goal():
    """
    Test that the remove_custom_goal() function in 
    restaurant_profile_manager.py can be used to remove
    a user's custom goal.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        old_goals = rpm.get_custom_goals()
        board_goals = rpm.get_bingo_board()["board"]
        found = False
        for i in range (0, len(old_goals)):
            if ObjectId(old_goals[i]['_id']) not in board_goals:
                found = True
                rpm.remove_custom_goal(old_goals[i]['_id'])
                break
        new_goals = rpm.get_custom_goals()
        assert (len(new_goals) == len(old_goals) and found == False) or \
               (len(new_goals) == (len(old_goals) - 1) and found == True)

def test_remove_custom_goal_on_board():
    """
    Test that the remove_custom_goal() function in 
    restaurant_profile_manager.py will not remove a goal
    that is on the board.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        old_goals = rpm.get_custom_goals()
        board_goals = rpm.get_bingo_board()["board"]
        for i in range (0, len(old_goals)):
            if ObjectId(old_goals[i]['_id']) in board_goals:
                rpm.remove_custom_goal(old_goals[i]['_id'])
                break
        new_goals = rpm.get_custom_goals()
        assert len(new_goals) == len(old_goals)

