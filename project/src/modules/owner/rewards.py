"""
This file houses the reward management interface for restaurant users.
It is used to interact with the rewards database and manipulate custom rewards for
restaurant users.
"""
from bson.objectid import ObjectId
from modules.database import QueryFailureException, UpdateFailureException


class RewardsManager():
    """
    This class generates a rewards manager capable of retrieving rewards from the rewards
    database and also manipulating custom rewards for restaurant users.
    """

    def __init__(self, restaurant_profile_manager):
        """
        Initialize a rewards manager using the provided restaurant profile manager.
        """
        self.rpm = restaurant_profile_manager

    def get_shared_rewards(self):
        """
        Return a list of all rewards that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.rpm.db.query('rewards')
        except QueryFailureException:
            print("There was an issue retrieving rewards.")
            return []

    def get_custom_rewards(self):
        """
        Gets custom rewards added by the user.
        """
        try:
            user = self.rpm.db.query('restaurant_users',
                                     {"username": self.rpm.get_id()})[0]
            return user["rewards"]
        except KeyError:  # New User, no rewards found
            return []
        except QueryFailureException:
            print("Something is wrong with the query")
            return []

    def get_rewards(self):
        """
        Return a list of all rewards that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_rewards()
        shared = self.get_shared_rewards()
        return custom + shared

    def add_custom_reward(self, reward):
        """
        Add a custom reward to the restaurant profile. If successful, return True.
        If reward already exists, return False.
        """
        try:
            rewards = self.get_rewards()
            in_database = [
                x['reward'] for x in rewards if x['reward'] == reward
            ]
            if in_database == []:
                try:
                    self.rpm.db.update('restaurant_users',
                                       {"username": self.rpm.get_id()}, {
                                           "$push": {
                                               "rewards": {
                                                   "_id": ObjectId(),
                                                   "reward": reward
                                               }
                                           }
                                       })
                    return True
                except UpdateFailureException:
                    print("There was an issue updating the rewards")
                    return False
        except QueryFailureException:
            print("Something is wrong with the query")
            return False
        return False

    def remove_custom_reward(self, reward_id):
        """
        Remove a restaurant user's custom reward that is not on their game board
        from their database and and returns
        "current" if the goal is on the current board, "future" if it is on
        the future board, "success" upon sucessful deletion, otherwise "fail"
        and throws an exception.
        """
        try:
            user = self.rpm.db.query("restaurant_users", {"username": self.rpm.get_id()})[0]
            rewards = user["bingo_board"]["board_reward"] if 'bingo_board' in user else []
            future_rewards = user["future_board"]["board_reward"] if 'future_board' in user else []
            if ObjectId(reward_id) in rewards:
                return "current"
            if ObjectId(reward_id) in future_rewards:
                return "future"
            self.rpm.db.update(
                'restaurant_users', {"username": self.rpm.get_id()},
                {"$pull": {
                    "rewards": {
                        "_id": ObjectId(reward_id)
                    }
                }})
            return "success"
        except QueryFailureException:
            print("There was an issue deleting the reward.")
            return "fail"
