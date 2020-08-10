"""
This file houses a goal/reward validator for restaurant users.
It is used to interact with goal completion and reward redemption information in the
database.
"""

from datetime import datetime
from bson.objectid import ObjectId
from modules.database import QueryFailureException, UpdateFailureException
from modules.owner.rewards import RewardsManager
from modules.owner.game_board import GameBoardManager


class Validator():
    """
    This class generates a validator capable of validating/verifying goals and rewards on behalf
    of a restaurant user.
    """

    def __init__(self, restaurant_profile_manager):
        """
        Initialize a validator using the given restaurant profile manager.
        """
        self.rpm = restaurant_profile_manager

    def add_reward_code(self, customer, reward_index):
        """
        Adds a reward code to the databases if there is a bingo on the board
        """
        owner = self.rpm.db.query('restaurant_users',
                                  {"username": self.rpm.get_id()})[0]
        reward_id = owner["bingo_board"]["board_reward"][reward_index]
        rewards = RewardsManager(self.rpm).get_rewards()
        text = ""
        for reward in rewards:
            if str(reward["_id"]) == str(reward_id):
                text = reward["reward"]
        code = str(customer) + "+" + str(reward_id) + "+" + str(
            reward_index) + "+" + str(datetime.now())
        try:
            if "client_rewards" not in owner:
                self.rpm.db.update('restaurant_users',
                                   {"username": self.rpm.get_id()}, {
                                       "$set": {
                                           "client_rewards": [{
                                               "redemption_code": code,
                                               "text": text,
                                               "is_redeemed": False
                                           }]
                                       }
                                   })
            else:
                self.rpm.db.update('restaurant_users',
                                   {"username": self.rpm.get_id()}, {
                                       "$push": {
                                           "client_rewards": {
                                               "redemption_code": code,
                                               "text": text,
                                               "is_redeemed": False
                                           }
                                       }
                                   })
            self.rpm.db.update(
                'customers', {
                    "username": customer,
                    "progress.restaurant_id": ObjectId(str(owner["_id"]))
                }, {
                    "$push": {
                        "progress.$.completed_rewards": {
                            "redemption_code": code,
                            "text": text,
                            "is_redeemed": False
                        }
                    }
                })
        except UpdateFailureException:
            print("There was an issue updating")

    def check_row(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the rows
        """
        start = int(position)
        counter = 0
        while (start % size) != 0:
            start = start - 1
        for i in range(start, start + size):
            for goal in goals:
                if i == int(goal["position"]):
                    counter = counter + 1
        if counter == size:
            self.add_reward_code(customer, int(int(position) / size) + 1)

    def check_col(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the columns
        """
        start = int(position) % size
        counter = 0
        for i in range(start, size * size, size):
            for goal in goals:
                if i == int(goal["position"]):
                    counter = counter + 1
        if counter == size:
            self.add_reward_code(customer, start + size + 1)

    def check_diagonal(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the diagonals
        """
        left = False
        right = False
        counter = 0
        start = int(position)
        while start >= 0:
            if start == 0:
                left = True
            start = start - (size + 1)

        start = int(position)
        while start >= (size - 1):
            if start == (size - 1):
                right = True
            start = start - (size - 1)

        if left:
            for i in range(0, size * size, size + 1):
                for goal in goals:
                    if i == int(goal["position"]):
                        counter = counter + 1
            if counter == size:
                self.add_reward_code(customer, size + size + 1)
        counter = 0
        if right:
            for i in range(size - 1, (size * size - (size - 1)), size - 1):
                for goal in goals:
                    if i == int(goal["position"]):
                        counter = counter + 1
                i = i + size - 1
            if counter == size:
                self.add_reward_code(customer, 0)

    def complete_goal(self, user, goal_id, position):
        """
        Adds a goal to the database that has been completed by the customer and returns
        a message depending on if it is successful or not.
        """
        try:
            owner_id = self.rpm.db.query(
                'restaurant_users', {"username": self.rpm.get_id()})[0]["_id"]
            size = self.rpm.db.query(
                'restaurant_users',
                {"username": self.rpm.get_id()})[0]["bingo_board"]["size"]
            user_profile = self.rpm.db.query('customers', {"username": user})[0]
            goals = []
            id_exists = False
            if "progress" in user_profile:
                for restaurant in user_profile["progress"]:
                    if restaurant["restaurant_id"] == owner_id:
                        goals = restaurant["completed_goals"]
                        for goal in goals:
                            if str(goal["_id"]
                                  ) == goal_id and position == goal["position"]:
                                return "This goal has already been completed!"
                        id_exists = True

            

            gbm = GameBoardManager(self.rpm)
            if not isinstance(int(position), int) or \
                    not (1 <= len(position) <= 2) or not (0 <= int(position) <= 24) or \
                    not str(gbm.get_bingo_board()["board"][int(position)]['_id']) == goal_id:
                return "Invalid QR code!"
            try:
                if "progress" in user_profile and id_exists:
                    self.rpm.db.update(
                        'customers', {
                            "username": user,
                            "progress.restaurant_id": ObjectId(owner_id)
                        }, {
                            "$push": {
                                "progress.$.completed_goals": {
                                    "_id": ObjectId(goal_id),
                                    "position": position,
                                    "date_completed": datetime.now()
                                }
                            }
                        })
                else:
                    self.rpm.db.update('customers', {"username": user}, {
                        "$push": {
                            "progress": {
                                "restaurant_id": ObjectId(owner_id),
                                "completed_goals": [{
                                    "_id": ObjectId(goal_id),
                                    "position": position,
                                    "date": datetime.now()
                                }],
                                "completed_rewards": []
                            }
                        }
                    })
                user_profile = self.rpm.db.query('customers',
                                                 {"username": user})[0]
                for restaurant in user_profile["progress"]:
                    if restaurant["restaurant_id"] == owner_id:
                        goals = restaurant["completed_goals"]
                self.check_col(position, size, user, goals)
                self.check_diagonal(position, size, user, goals)
                self.check_row(position, size, user, goals)
                return "Successfully marked as completed!"
            except UpdateFailureException:
                print("There was an issue updating")
                return "Error"
        except QueryFailureException:
            print("Something is wrong with the query")
            return "Error"
        return "Error"

    def complete_reward(self, user, code):
        """
        Adds a reward to the database that has been completed by the customer and returns
        a message depending on if it is successful or not.
        """
        try:
            owner = self.rpm.db.query('restaurant_users',
                                      {"username": self.rpm.get_id()})[0]
            user_profile = self.rpm.db.query('customers', {"username": user})[0]
            in_user = False
            counter = -1
            if "progress" in user_profile:
                for restaurant in user_profile["progress"]:
                    counter += 1
                    if restaurant["restaurant_id"] == owner["_id"]:
                        restaurant_index = counter
                        rewards = restaurant['completed_rewards']
                        counter = -1
                        for reward in rewards:
                            counter += 1
                            if reward["redemption_code"] == code:
                                text = reward["text"]
                                in_user = True
                                customer_index = counter
                                if "redemption_date" in reward:
                                    return "Code has already been redeemed!"
                if not in_user:
                    return "Invalid QR code!"
            counter = -1
            for reward in owner["client_rewards"]:
                counter += 1
                if reward["redemption_code"] == code:
                    owner_index = counter

            self.rpm.db.update(
                'restaurant_users', {
                    "username": self.rpm.get_id(),
                    "client_rewards.redemption_code": code
                }, {
                    "$set": {
                        "client_rewards." + str(owner_index): {
                            "redemption_code": code,
                            "text": text,
                            "is_redeemed": True,
                            "redemption_date": datetime.now()
                        }
                    }
                })

            self.rpm.db.update(
                'customers', {
                    "username": user,
                    "progress.restaurant_id": ObjectId(str(owner["_id"])),
                    "progress.completed_rewards.redemption_code": code
                }, {
                    "$set": {
                        "progress." + str(restaurant_index) +\
                            ".completed_rewards." + str(customer_index):
                            {
                                "redemption_code": code,
                                "text": text,
                                "is_redeemed": True,
                                "redemption_date": datetime.now()
                            }
                    }
                })

            return "Successfully marked as redeemed!"
        except QueryFailureException:
            print("Something is wrong with the query")
            return "Error"
        return "Error"
