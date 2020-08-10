"""
This file houses the restaurant game board management interface.
It is used to interact with a restaurant profile's game boards.
"""

import copy
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from bson.errors import InvalidId
from modules.database import Database, QueryFailureException, UpdateFailureException
from modules.owner.goals import GoalsManager
from modules.owner.rewards import RewardsManager
from modules.owner.restaurant_profile_manager import RestaurantProfileManager


class GameBoardManager():
    """
    This class generates a game board manager manager capable of retrieving and updating
    a restaurant owner's bingo board. It includes expiry date functionality.
    """

    def __init__(self, restaurant_profile_manager):
        """
        Initialize a board manager using the provided restaurant profile manager.
        """
        self.rpm = restaurant_profile_manager

    def get_bingo_board(self):
        """
        Return the current restaurant user's bingo board. The board will include
        text info for goals and rewards.
        """
        try:
            goals = GoalsManager(self.rpm).get_goals()
            rewards = RewardsManager(self.rpm).get_rewards()
            board = self.rpm.db.query(
                "restaurant_users",
                {"_id": self.rpm.get_id()})[0]["bingo_board"]

            board["board"] = [
                copy.deepcopy(goal)
                for index in board["board"]
                for goal in goals
                if index == goal["_id"]
            ]

            board["board_reward"] = [
                copy.deepcopy(reward)
                for index in board["board_reward"]
                for reward in rewards
                if index == reward["_id"]
            ]
            return board
        except (QueryFailureException, IndexError, KeyError):
            print("Something's wrong with the query.")
            return {}

    def get_restaurant_board_by_id(self, rest_id):
        """
        Return a restaurant board given a restaurant database id. The board will include
        text info for goals and rewards.
        """
        try:
            restaurant = self.rpm.db.query("restaurant_users",
                                           {"_id": ObjectId(rest_id)})[0]
            temp_rpm = self.rpm
            self.rpm = RestaurantProfileManager(restaurant["username"])
            board = self.get_bingo_board()
            self.rpm = temp_rpm
            return board
        except (QueryFailureException, IndexError):
            print("Something's wrong with the query.")
            return {}

    def set_bingo_board(self, bingo_board):
        """
        Update the restaurant user's bingo board using the board.
        """
        try:
            # convert the date string to a python date
            if not isinstance(bingo_board["expiry_date"], datetime):
                date = [
                    int(part) for part in bingo_board["expiry_date"].split("/")
                ]
                bingo_board["expiry_date"] = datetime(date[2], date[0], date[1],
                                                      23, 59, 59)

            # convert ids to object ids
            bingo_board["board"] = Database.replace_object_id(
                bingo_board["board"])
            bingo_board["board_reward"] = Database.replace_object_id(
                bingo_board["board_reward"])

            # if new user, update current board as well as future board
            boards = {"future_board": bingo_board}
            if self.get_future_board()["name"] == "":
                boards["bingo_board"] = copy.deepcopy(bingo_board)
                boards["future_board"]["expiry_date"] = boards["future_board"]["expiry_date"] + \
                                                        timedelta(days=90)

            self.rpm.db.update('restaurant_users',
                               {"username": self.rpm.get_id()},
                               {'$set': boards})
        except (UpdateFailureException, KeyError):
            print("There was an issue updating a bingo board.")

    def update_board(self, obj_id):
        """
        Checks all public restaurant user's bingo boards and replaces expired
        boards with future game boards. If no future board exists, expiration
        date is increased by 90 days.
        """
        try:
            user = self.rpm.db.query('restaurant_users', {'_id': obj_id})
            reset = 90  # expiration date deafault is set to 90 days
            if 'expiry_date' in user[0]['bingo_board']:
                if datetime.now() >= user[0]['bingo_board'][
                        'expiry_date']:  # expired current board
                    if 'future_board' in user[0]:
                        future_exp = user[0]['future_board']['expiry_date']
                        if future_exp <= datetime.now():  # expired future goal
                            future_exp = datetime.now() + timedelta(days=reset)
                        user[0]['future_board'][
                            'expiry_date'] = future_exp  # updates future exp date
                        self.rpm.db.update(  # updates current board in db
                            'restaurant_users',
                            {'username': user[0]['username']},
                            {'$set': {
                                'bingo_board': user[0]['future_board']
                            }})
                        user[0]['future_board'][  # updates future board in db
                            'expiry_date'] = future_exp + timedelta(days=reset)
                        self.rpm.db.update(
                            'restaurant_users',
                            {'username': user[0]['username']},
                            {'$set': {
                                'future_board': user[0]['future_board']
                            }})
                    customers = self.rpm.db.query('customers')
                    for customer in customers:
                        if 'progress' in customer:
                            for item in customer['progress']:
                                # checks for completed goals corresponding to expired board
                                if item['restaurant_id'] == ObjectId(
                                        obj_id) and 'completed_goals' in item:
                                    # removes current goals in customer profiles
                                    self.rpm.db.update(
                                        'customers', {
                                            "username": customer['username'],
                                            "progress.restaurant_id": obj_id
                                        }, {
                                            "$set": {
                                                "progress.$.completed_goals": [
                                                ]
                                            }
                                        })
        except UpdateFailureException:
            print("There was an issue updating")
        except KeyError:
            print("No current board")

    def get_future_board(self):
        """
        Return the future board attached to the current restaurant user.
        """
        try:
            profile = self.rpm.db.query('restaurant_users',
                                        {"username": self.rpm.get_id()})
            return profile[0]["future_board"]
        except KeyError:  # New User, no future board found
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }
        except (QueryFailureException, IndexError):
            print("There was an issue retrieving a bingo board.")
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }

    def get_current_board_expiry(self):
        """
        Return the expiry date of the user's active board.
        """
        try:
            profile = self.rpm.db.query('restaurant_users',
                                        {"username": self.rpm.get_id()})
            return profile[0]["bingo_board"]["expiry_date"]
        except (QueryFailureException, IndexError, KeyError, InvalidId):
            return None
