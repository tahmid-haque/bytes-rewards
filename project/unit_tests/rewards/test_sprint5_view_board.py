"""
This file houses the unit test suite for the view board interface on the rewards app.
"""

import os
import sys
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from bson.objectid import ObjectId
from rewards_app import app
from modules.owner.game_board import GameBoardManager
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.owner.public_profile import PublicProfileModifier
from modules.customer.customer_profile_manager import CustomerProfileManager
from modules.customer.favourite import *
from modules.customer.customer_board import *

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


def test_get_board_by_id():
    """
    Test that get_restaurant_board_by_id() returns the correct bingo board information.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        bpm = GameBoardManager(rpm)
        board = bpm.get_restaurant_board_by_id("5f15c084143cb39bfc5619b8")
        assert board["name"] == "KFC Rewards"

        assert board["board"][0] == {
            "_id": ObjectId("5f15c1b3143cb39bfc5619b9"),
            "goal": "resignation"
        }
        assert board["board"][12] == {
            "_id": ObjectId("5f15c1de143cb39bfc5619c5"),
            "goal": "inch"
        }
        assert board["board"][24] == {
            "_id": ObjectId("5f15c200143cb39bfc5619d1"),
            "goal": "transmission"
        }

        assert board["board_reward"][0] == {
            "_id": ObjectId("5f03aa437aae4a086d810107"),
            "reward": "One free drink refill"
        }
        assert board["board_reward"][5] == {
            "_id": ObjectId("5f03aa0b7aae4a086d810103"),
            "reward": "Free appetizer"
        }
        assert board["board_reward"][11] == {
            "_id": ObjectId("5f03aa437aae4a086d810107"),
            "reward": "One free drink refill"
        }


def test_set_board_progress_no_progress():
    """
    Test that set_board_progress() updates all goals on a bingo board to incomplete.
    """
    rpm = RestaurantProfileManager("")
    bpm = GameBoardManager(rpm)
    board = bpm.get_restaurant_board_by_id("5f15c084143cb39bfc5619b8")
    cpm = CustomerProfileManager("newuser")

    set_board_progress(cpm, board, "5f15c084143cb39bfc5619b8")

    for goal in board["board"]:
        assert not goal["is_complete"]


def test_set_board_progress_some_progress():
    """
    Test that set_board_progress() updates all goals on a bingo board to the correct progress info.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("")
        bpm = GameBoardManager(rpm)
        board = bpm.get_restaurant_board_by_id("5f15c084143cb39bfc5619b8")
        cpm = CustomerProfileManager("unittestuser2")

        set_board_progress(cpm, board, "5f15c084143cb39bfc5619b8")

        print(board["board"])
        for i in range(len(board["board"])):
            if i in [0, 8, 14, 23]:
                assert board["board"][i]["is_complete"] or board["board"][i]["is_bingo"]
            else:
                assert not board["board"][i]["is_complete"]


def test_view_board_goal_qr_code_data(client):
    """
    Test that the data for goal QR codes are being set correctly.
    """
    with app.app_context():
        client.post("/login",
                    data={
                        "username": "unittestuser",
                        "password": "Password!"
                    })
        res = client.get("/restaurants/5f0df6a10bb07c8199d4405a/board",
                         follow_redirects=True)

        rpm = RestaurantProfileManager("")
        bpm = GameBoardManager(rpm)
        board = bpm.get_restaurant_board_by_id("5f0df6a10bb07c8199d4405a")

        for i in range(len(board["board"])):
            assert str.encode("unittestuser+{}+{}".format(board["board"][i]["_id"],
                                                          i)) in res.data
