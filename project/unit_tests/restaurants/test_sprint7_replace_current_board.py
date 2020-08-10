"""
This file houses the unit test for replacing expired game boards.
"""

import os
import sys
import copy
from datetime import datetime, timedelta
import pytest
sys.path.insert(1, os.path.join(os.path.dirname(__file__),
                                '../../src'))  # Import the src folder
from restaurants_app import app
from modules.owners.restaurant_profile_manager import RestaurantProfileManager
from modules.owners.public_profile import PublicProfileModifier
from modules.owner.game_board import GameBoardManager

@pytest.fixture
def client():
    """
    Initialize flask app to indicate a testing environment.
    Returns the testing client.
    """
    app.config['TESTING'] = True
    return app.test_client()


def test_update_current_with_future():
    """
    Tests that update_board replaces an expired bingo board with a future board
    that has an expiry date that is in the future and updates the future board
    to have an expiration date of 90 more days, and customer's completed goals
    are removed.
    """
    with app.app_context():
        rpm = RestaurantProfileManager('testuser')
        pm = PublicProfileModifier(rpm)
        gm = GameBoardManager(rpm)
        public_users = pm.get_public_users()
        expired_board_user = []
        current_boards = []
        actual_future = []
        expected_boards = []
        expected_future = []
        customer_update = True
        for user in public_users:
            # expired current but not future board
            if 'expiry_date' in user['bingo_board'] and user['bingo_board'][
                    'expiry_date'] < datetime.now(
                    ) and user['future_board']['expiry_date'] > datetime.now():
                expired_board_user.append(user['_id'])
                # expected current board is future board
                expected_boards.append(user['future_board'])
                to_add = copy.deepcopy(user['future_board'])
                to_add['expiry_date'] = user['future_board'][
                    'expiry_date'] + timedelta(days=90)
                # expected future board has increased exp date
                expected_future.append(to_add)
                gm.update_board(user['_id'])
        public_users = pm.get_public_users()
        for user in public_users:
            #searches for users whose boards were updated
            if user['_id'] in expired_board_user:
                current_boards.append(user['bingo_board'])
                actual_future.append(user['future_board'])
        customers = rpm.db.query('customers')
        for c in customers:
            if 'progress' in c:
                for rest in c['progress']:
                    # searches for customers whose progress was updated
                    if rest['restaurant_id'] in expired_board_user and 'completed_goals' in rest:
                        # completed goals were not updated
                        if len(rest['completed_goals']) > 0:
                            customer_update = False
        assert current_boards == expected_boards and actual_future == expected_future and customer_update


def test_update_expired_future_expiry_date():
    """
    Tests update_board will update an expired future game board
    to be 90 days from current time.
    """
    with app.app_context():
        rpm = RestaurantProfileManager('testuser')
        pm = PublicProfileModifier(rpm)
        gm = GameBoardManager(rpm)
        public_users = pm.get_public_users()
        expired_board = []
        expected = True
        for user in public_users:
            # expired current and future board
            if 'expiry_date' in user['bingo_board'] and user['bingo_board'][
                    'expiry_date'] < datetime.now(
                    ) and user['future_board']['expiry_date'] < datetime.now():
                expired_board.append(user)
                gm.update_board(user['_id'])
        public_users = rpm.get_public_users()
        for expired_user in expired_board:
            for user in public_users:
                #searches for users whose boards were updated
                if user['username'] == expired_user['username']:
                    # future exp date was not updated
                    if user['future_board']['expiry_date'] < datetime.now():
                        expected = False
        assert expected
