from bson.objectid import ObjectId
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


def test_get_rewards_new_user():
    """
    Test that the get_bingo_board() function in restaurant_profile_manager.py 
    retrieves an empty board and reward list when a new user is detected.
    """
    rpm = RestaurantProfileManager("newuser")
    rewards = (rpm.get_bingo_board())["board_reward"]
    assert rewards == []


def test_get_shared_rewards():
    """
    Test that get_shared_rewards() function in restaurant_profile_manager.py
    retrieves the list of shared rewards from the database.
    """
    rpm = RestaurantProfileManager("vchang")
    shared = rpm.get_shared_rewards()
    expected_shared = [{
        '_id': ObjectId('5f03a9df7aae4a086d810100'),
        'reward': '$5 off a purchase of $30+'
    }, {
        '_id': ObjectId('5f03a9fd7aae4a086d810102'),
        'reward': 'Free drink'
    }, {
        '_id':
            ObjectId('5f03aa287aae4a086d810105'),
        'reward':
            'Buy one entree, get another 50% off (of lesser or equal value)'
    }, {
        '_id': ObjectId('5f03aa1a7aae4a086d810104'),
        'reward': 'Free dessert'
    }, {
        '_id': ObjectId('5f03a9c87aae4a086d8100ff'),
        'reward': '$10 off a purchase of $50+'
    }, {
        '_id': ObjectId('5f03aa0b7aae4a086d810103'),
        'reward': 'Free appetizer'
    }, {
        '_id': ObjectId('5f03a9967aae4a086d8100fd'),
        'reward': '10% off a purchase'
    }, {
        '_id': ObjectId('5f03aa377aae4a086d810106'),
        'reward': '$3 off any entree'
    }, {
        '_id': ObjectId('5f03aa437aae4a086d810107'),
        'reward': 'One free drink refill'
    }, {
        '_id': ObjectId('5f03aa507aae4a086d810108'),
        'reward': 'All desserts $6 each'
    }, {
        '_id': ObjectId('5f03a9b57aae4a086d8100fe'),
        'reward': '15% off a purchase'
    }, {
        '_id': ObjectId('5f03a9ec7aae4a086d810101'),
        'reward': '$5 gift voucher'
    }]
    assert shared == expected_shared


def test_get_rewards_old_user():
    """
    Test that get_rewards() inrestaurant_profile_manager.py for an existin
    user retrieves a list of their available rewards.
    """
    rpm = RestaurantProfileManager("vchang")
    rewards = rpm.get_rewards()
    expected_rewards = [{
        '_id': ObjectId('5f03a9df7aae4a086d810100'),
        'reward': '$5 off a purchase of $30+'
    }, {
        '_id': ObjectId('5f03a9fd7aae4a086d810102'),
        'reward': 'Free drink'
    }, {
        '_id':
            ObjectId('5f03aa287aae4a086d810105'),
        'reward':
            'Buy one entree, get another 50% off (of lesser or equal value)'
    }, {
        '_id': ObjectId('5f03aa1a7aae4a086d810104'),
        'reward': 'Free dessert'
    }, {
        '_id': ObjectId('5f03a9c87aae4a086d8100ff'),
        'reward': '$10 off a purchase of $50+'
    }, {
        '_id': ObjectId('5f03aa0b7aae4a086d810103'),
        'reward': 'Free appetizer'
    }, {
        '_id': ObjectId('5f03a9967aae4a086d8100fd'),
        'reward': '10% off a purchase'
    }, {
        '_id': ObjectId('5f03aa377aae4a086d810106'),
        'reward': '$3 off any entree'
    }, {
        '_id': ObjectId('5f03aa437aae4a086d810107'),
        'reward': 'One free drink refill'
    }, {
        '_id': ObjectId('5f03aa507aae4a086d810108'),
        'reward': 'All desserts $6 each'
    }, {
        '_id': ObjectId('5f03a9b57aae4a086d8100fe'),
        'reward': '15% off a purchase'
    }, {
        '_id': ObjectId('5f03a9ec7aae4a086d810101'),
        'reward': '$5 gift voucher'
    }]
    assert rewards == expected_rewards


def test_get_rewards_from_board():
    """
    Test that the get_bingo_board() function in restaurant_profile_manager.py 
    retrieves a user's list of rewards on their bingo board.
    """
    rpm = RestaurantProfileManager("unittestuser")
    board = rpm.get_bingo_board()
    rewards = board["board_reward"]
    expected_rewards = [
        ObjectId('5f03aa437aae4a086d810107'),
        ObjectId('5f03a9b57aae4a086d8100fe'),
        ObjectId('5f03a9c87aae4a086d8100ff'),
        ObjectId('5f03a9ec7aae4a086d810101'),
        ObjectId('5f03aa507aae4a086d810108'),
        ObjectId('5f03a9c87aae4a086d8100ff'),
        ObjectId('5f03aa287aae4a086d810105'),
        ObjectId('5f03a9967aae4a086d8100fd'),
        ObjectId('5f03a9fd7aae4a086d810102'),
        ObjectId('5f03a9fd7aae4a086d810102'),
        ObjectId('5f03a9fd7aae4a086d810102'),
        ObjectId('5f03a9ec7aae4a086d810101')
    ]
    assert rewards == expected_rewards


def test_index_route_no_login(client):
    """
    Test that index page does not load unless user is logged in.
    """
    res = client.get("/", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_index_route_logged_in(client):
    """
    Test that index page loads when the user is logged in.
    """
    client.post("/login",
                data={
                    "username": "unittestuser",
                    "password": "Jake1234"
                })
    res = client.get("/", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data
    assert b"Edit Profile" in res.data


def test_save_rewards_no_login(client):
    """
    Test that a user is unable to save a game board unless they are logged in.
    """
    res = client.post("/board/save", follow_redirects=True)
    assert b'Please log in to access this page' in res.data


def test_set_board_rewards():
    """
    Test that the set_bingo_board() function in restaurant_profile_manager.py 
    can be used to update a user's list of rewards.
    """
    rpm = RestaurantProfileManager("vchang")
    old_rewards = (rpm.get_bingo_board())["board_reward"]
    board = (rpm.get_bingo_board())["board"]
    name = (rpm.get_bingo_board())["name"]

    new_rewards = [
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b'),
        ObjectId('5ef50127ccd1e88ead4cd07b')
    ]
    rpm.set_bingo_board(name, board, new_rewards)

    assert (rpm.get_bingo_board())["board_reward"] == new_rewards

    rpm.set_bingo_board(name, board, old_rewards)
