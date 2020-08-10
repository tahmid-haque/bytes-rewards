"""
This file houses the unit test suite for the clearing a full customer bingo board"
"""

import os
import sys
import pytest

sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from rewards_app import app
from modules.restaurant_profile_manager import RestaurantProfileManager
from modules.customer.customer_profile_manager import CustomerProfileManager
from modules.database import Database
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

@pytest.fixture
def db(client):
    """
    Return a database instance.
    """
    with app.app_context():
        return Database.get_instance()

def test_reset_board(db):
    """
    Test that reset board resets goals on the board when the board is full.
    """
    rpm = RestaurantProfileManager("boardtest3x3")
    cpm = CustomerProfileManager("tester2")
    
    board = rpm.get_bingo_board()
    for i in range(board['size']):
        rpm.complete_goal("tester", board['board'][i], str(i))
    
    rest_id = rpm.get_restaurant_id()
    reset_complete_board(cpm, rest_id)
    
    rest_board = db.query("customers", {
        "username": "tester2",
        "progress.restaurant_id": rest_id
        })
        
    user_board = [x for x in rest_board[0]['progress'] if x['restaurant_id'] == rest_id]
    
    assert len(user_board[0]["completed_goals"]) == 0
    