"""
This file houses the unit test for remove custom reward backend.
"""

import os
import sys
import pytest
from bson.objectid import ObjectId
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from restaurants_app import app
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.rewards import RewardsManager
from modules.owner.game_board import GameBoardManager


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


def test_remove_custom_reward():
    """
    Test that the remove_custom_reward() function in
    restaurant_profile_manager.py can be used to remove
    a user's custom reward.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        rm = RewardsManager(rpm)
        gm = GameBoardManager(rpm)
        old_rewards = rm.get_custom_rewards()
        board_rewards = gm.get_bingo_board()["board_reward"]
        found = False
        for i in range(0, len(old_rewards)):
            if ObjectId(old_rewards[i]['_id']) not in board_rewards:
                found = True
                rm.remove_custom_reward(old_rewards[i]['_id'])
                break
        new_rewards = rm.get_custom_rewards()
        assert (len(new_rewards) == len(old_rewards) and not found) or \
               (len(new_rewards) == (len(old_rewards) - 1) and found)


def test_remove_custom_reward_on_board():
    """
    Test that the remove_custom_reward() function in
    restaurant_profile_manager.py will not remove a goal
    that is on the board.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("vchang")
        rm = RewardsManager(rpm)
        gm = GameBoardManager(rpm)
        old_rewards = rm.get_custom_rewards()
        board_rewards = gm.get_bingo_board()["board_reward"]
        for i in range(0, len(old_rewards)):
            if ObjectId(old_rewards[i]['_id']) in board_rewards or ObjectId(old_rewards[i]['_id']) in future_rewards:
                rm.remove_custom_reward(old_rewards[i]['_id'])
                break
        new_rewards = rm.get_custom_rewards()
        assert len(new_rewards) == len(old_rewards)

def test_delete_custom_reward_not_logged_in(client):
    """
    Test that a user cannot delete a reward when they're not logged in.
    """
    some_id = {"deleted-reward": "5f18ca9049a4855e3b0ca7b5"} # Utilize an actual existing ID.
    res = client.post("/customize/delete-reward", data=some_id, follow_redirects=True)
    assert b"Please log in to access this page" in res.data
