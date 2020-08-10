"""
This file houses the unit test suite for the board editor interface.
"""

import os
import sys
from datetime import datetime
import pytest
from bson.objectid import ObjectId
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder

from restaurants_app import app
from modules.owner.restaurant_profile_manager import RestaurantProfileManager
from modules.database import Database
from modules.owner.game_board import GameBoardManager


@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def get_board():
    """
    Returns a bingo board for use in testing.
    """
    return {
        "name":
            "A Random Board",
        "size":
            3,
        "expiry_date":
            "05/26/2021",
        "board": [
            "5ef50183ccd1e88ead4cd081", "5ef501f1ccd1e88ead4cd089",
            "5ef5010fccd1e88ead4cd079", "5ef50134ccd1e88ead4cd07c",
            "5ef50183ccd1e88ead4cd081", "5ef501b9ccd1e88ead4cd084",
            "5ef500edccd1e88ead4cd078", "5ef50155ccd1e88ead4cd07e",
            "5ef500edccd1e88ead4cd078"
        ],
        "board_reward": [
            "5f03aa287aae4a086d810105", "5f03a9fd7aae4a086d810102",
            "5f03aa377aae4a086d810106", "5f03a9df7aae4a086d810100",
            "5f03aa507aae4a086d810108", "5f03aa377aae4a086d810106",
            "5f03a9df7aae4a086d810100", "5f03aa507aae4a086d810108"
        ]
    }


def get_database_board():
    """
    Returns the expected database bingo board for use in testing.
    """
    return {
        "name":
            "A Random Board",
        "size":
            3,
        "expiry_date":
            datetime(2021, 5, 26, 23, 59, 59),
        "board": [
            ObjectId("5ef50183ccd1e88ead4cd081"),
            ObjectId("5ef501f1ccd1e88ead4cd089"),
            ObjectId("5ef5010fccd1e88ead4cd079"),
            ObjectId("5ef50134ccd1e88ead4cd07c"),
            ObjectId("5ef50183ccd1e88ead4cd081"),
            ObjectId("5ef501b9ccd1e88ead4cd084"),
            ObjectId("5ef500edccd1e88ead4cd078"),
            ObjectId("5ef50155ccd1e88ead4cd07e"),
            ObjectId("5ef500edccd1e88ead4cd078")
        ],
        "board_reward": [
            ObjectId("5f03aa287aae4a086d810105"),
            ObjectId("5f03a9fd7aae4a086d810102"),
            ObjectId("5f03aa377aae4a086d810106"),
            ObjectId("5f03a9df7aae4a086d810100"),
            ObjectId("5f03aa507aae4a086d810108"),
            ObjectId("5f03aa377aae4a086d810106"),
            ObjectId("5f03a9df7aae4a086d810100"),
            ObjectId("5f03aa507aae4a086d810108")
        ]
    }


@pytest.fixture
def db(client):
    """
    Return a database instance.
    """
    with app.app_context():
        return Database.get_instance()


def test_set_bingo_board_new_user(db):
    """
    Test that set_bingo_board() sets both the current and future boards for users with no current
    board data.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("newuser")
        gm = GameBoardManager(rpm)
        gm.set_bingo_board(get_board())
        user = db.query("restaurant_users", {"username": "newuser"})[0]

        db_board = get_database_board()
        assert user["bingo_board"] == db_board

        db_board["expiry_date"] = datetime(2021, 8, 24, 23, 59, 59)
        assert user["future_board"] == db_board

        # reset new user's boards
        db.update("restaurant_users", {"username": "newuser"},
                  {"$unset": {
                      "bingo_board": "",
                      "future_board": ""
                  }})


def test_set_bingo_board_old_user(db):
    """
    Test that set_bingo_board() sets only the future board for users that have previous
    board data.
    """
    with app.app_context():
        prev_user = db.query("restaurant_users",
                             {"username": "boardeditoruser"})[0]

        rpm = RestaurantProfileManager("boardeditoruser")
        gm = GameBoardManager(rpm)
        gm.set_bingo_board(get_board())
        user = db.query("restaurant_users", {"username": "boardeditoruser"})[0]

        assert user["future_board"] == get_database_board()
        assert user["bingo_board"] == prev_user["bingo_board"]

        # reset user's boards to pre-test
        db.update("restaurant_users", {"username": "boardeditoruser"},
                  {"$set": prev_user})


def test_get_future_board_new_user():
    """
    Test that get_future_board() retrieves an empty board for a new user.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("newuser")
        gm = GameBoardManager(rpm)
        assert gm.get_future_board() == {
            "board": [],
            "name": "",
            "board_reward": [],
            "expiry_date": None,
            "size": 4
        }


def test_get_future_board_old_user():
    """
    Test that get_future_board() retrieves the correct future board for a user with board data.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("boardeditoruser")
        gm = GameBoardManager(rpm)
        assert gm.get_future_board() == {
            "name":
                "My 3x3",
            "size":
                3,
            "expiry_date":
                datetime(2020, 11, 27, 23, 59, 59),
            "board": [
                ObjectId("5ef50183ccd1e88ead4cd081"),
                ObjectId("5ef501f1ccd1e88ead4cd089"),
                ObjectId("5ef5010fccd1e88ead4cd079"),
                ObjectId("5ef50134ccd1e88ead4cd07c"),
                ObjectId("5ef50183ccd1e88ead4cd081"),
                ObjectId("5ef501b9ccd1e88ead4cd084"),
                ObjectId("5ef50155ccd1e88ead4cd07e"),
                ObjectId("5ef501b9ccd1e88ead4cd084"),
                ObjectId("5ef500edccd1e88ead4cd078")
            ],
            "board_reward": [
                ObjectId("5f03a9fd7aae4a086d810102"),
                ObjectId("5f03aa377aae4a086d810106"),
                ObjectId("5f03aa507aae4a086d810108"),
                ObjectId("5f03a9df7aae4a086d810100"),
                ObjectId("5f03aa377aae4a086d810106"),
                ObjectId("5f03a9df7aae4a086d810100"),
                ObjectId("5f03aa287aae4a086d810105"),
                ObjectId("5f03aa507aae4a086d810108")
            ]
        }


def test_get_current_expiry_new_user():
    """
    Test that get_current_board_expiry() returns None for a new user.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("newuser")
        gm = GameBoardManager(rpm)
        assert gm.get_current_board_expiry() is None


def test_get_current_expiry_old_user():
    """
    Test that get_current_board_expiry() returns the correct expiry date for a user
    with board data.
    """
    with app.app_context():
        rpm = RestaurantProfileManager("boardeditoruser")
        gm = GameBoardManager(rpm)
        assert gm.get_current_board_expiry() == datetime(
            2020, 11, 23, 23, 59, 59)


def test_edit_board_no_login(client):
    """
    Test that board editor page does not load unless user is logged in.
    """
    res = client.get("/board/edit", follow_redirects=True)
    assert b"Please log in to access this page" in res.data


def test_edit_board_logged_in(client):
    """
    Test that board editor page loads when a user is logged in.
    """
    client.post("/login", data={"username": "newuser", "password": "Password!"})
    res = client.get("/board/edit", follow_redirects=True)
    assert b"Please log in to access this page" not in res.data
    assert b"Board Title" in res.data
