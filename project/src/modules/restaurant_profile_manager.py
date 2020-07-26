"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""

from bson.objectid import ObjectId
from modules.profile_manager import ProfileManager
from modules.database import Database, QueryFailureException, UpdateFailureException


class RestaurantProfileManager(ProfileManager):
    """
    This class generates a restaurant profile manager, capable of managing
    one restaurant profile. Some of the things it manages include goals and
    bingo boards. It inherits from ProfileManager to perform basic
    creation/load operations.
    """

    def __init__(self, username):
        """
        Initialize a restaurant user profile using the username.
        """
        ProfileManager.__init__(self, username, 'restaurant_users')

    def get_shared_goals(self):
        """
        Return a list of all goals that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.db.query('goals')
        except QueryFailureException:
            print("There was an issue retrieving goals.")
            return []

    def get_goals(self):
        """
        Return a list of all goals that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_goals()
        shared = self.get_shared_goals()
        return custom + shared

    def get_bingo_board(self):
        """
        Return a bingo board attached to the current restaurant user.
        """
        try:
            profile = self.db.query('restaurant_users', {"username": self.id})
            return profile[0]["bingo_board"]
        except KeyError:  # New User, no bingo board found
            return {"name": "", "board": [], "board_reward": []}
        except (QueryFailureException, IndexError):
            print("There was an issue retrieving a bingo board.")
            return {"name": "", "board": [], "board_reward": []}

    def set_bingo_board(self, name, board, board_reward):
        """
        Update the restaurant user's bingo board using the given name and
        board.
        """
        try:
            board = Database.replace_object_id(board)
            board_reward = Database.replace_object_id(board_reward)
            self.db.update('restaurant_users', {"username": self.id}, {
                '$set': {
                    "bingo_board": {
                        "name": name,
                        "board": board,
                        "board_reward": board_reward
                    }
                }
            })
        except UpdateFailureException:
            print("There was an issue updating a bingo board.")

    def get_shared_rewards(self):
        """
        Return a list of all rewards that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.db.query('rewards')
        except QueryFailureException:
            print("There was an issue retrieving rewards.")
            return []

    def get_rewards(self):
        """
        Return a list of all rewards that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_rewards()
        shared = self.get_shared_rewards()
        return custom + shared

    def get_profile(self):
        """
        Return the restaurant user's profile.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["profile"]
        except KeyError:  # New User, no profile found
            return {}
        except (QueryFailureException, IndexError):
            print("There was an issue retrieving a profile")
            return {}

    def update_profile(self, profile):
        """
        Update the restaurant user's profile using the data provided in profile.
        """
        profile['is_public'] = 'is_public' in profile
        try:
            self.db.update('restaurant_users', {"username": self.id},
                           {'$set': {
                               "profile": profile
                           }})
        except UpdateFailureException:
            print("There was an issue updating a profile.")

    def get_public_users(self):
        """
        Get all restaurant users that have a public profile.
        """
        try:
            restaurant_owners = self.db.query('restaurant_users',
                                              {'profile.is_public': True})
            return restaurant_owners
        except QueryFailureException:
            print("Something's wrong with the query.")
            return []

    def get_public_profiles(self):
        """
        Get all restaurant profiles that are set to public.
        """
        users = self.get_public_users()
        return {owner["_id"]: owner["profile"] for owner in users}

    def get_custom_goals(self):
        """
        Gets custom goals added by the user.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["goals"]
        except KeyError:  # New User, no goals found
            return []
        except (QueryFailureException, IndexError):
            print("Something is wrong with the query")
            return []

    def add_custom_goal(self, goal):
        """
        Add a custom goal to the restaurant profile. If successful, return True.
        If goal already exists, return False.
        """
        goals = self.get_goals()
        in_database = [x['goal'] for x in goals if x['goal'] == goal]
        if in_database == []:
            try:
                self.db.update(
                    'restaurant_users', {"username": self.id},
                    {"$push": {
                        "goals": {
                            "_id": ObjectId(),
                            "goal": goal
                        }
                    }})
                return True
            except UpdateFailureException:
                print("There was an issue updating the goals")
                return False
        return False

    def remove_custom_goal(self, goal_id):
        """
        Remove a restaurant user's custom goal from their database and returns
        True upon success; throws exception and returns False otherwise.
        """
        try:
            goals = self.get_bingo_board()["board"]
            if ObjectId(goal_id) in goals:
                return False
            self.db.update('restaurant_users', {"username": self.id},
                           {"$pull": {
                               "goals": {
                                   "_id": ObjectId(goal_id)
                               }
                           }})
            return True
        except QueryFailureException:
            print("There was an issue deleting the goal.")
            return False

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
                    self.db.update('restaurant_users', {"username": self.id}, {
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

    def get_custom_rewards(self):
        """
        Gets custom rewards added by the user.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["rewards"]
        except KeyError:  # New User, no rewards found
            return []
        except QueryFailureException:
            print("Something is wrong with the query")
            return []

    def remove_custom_reward(self, reward_id):
        """
        Remove a restaurant user's custom reward that is not on their game board
        from their database and returns
        True upon success; throws exception and returns False otherwise.
        """
        try:
            rewards = self.get_bingo_board()["board_reward"]
            if ObjectId(reward_id) in rewards:
                return False
            self.db.update('restaurant_users', {"username": self.id}, {
                "$pull": {
                    "rewards": {
                        "_id": ObjectId(reward_id)
                    }
                }
            })
            return True
        except QueryFailureException:
            print("There was an issue deleting the reward.")
            return False

    def get_restaurant_board_by_id(self, rest_id):
        """
        Return a restaurant board given a restaurant database id. The board will include
        text info for goals and rewards.
        """
        try:
            temp_id = self.id
            restaurant = self.db.query("restaurant_users",
                                       {"_id": ObjectId(rest_id)})[0]
            self.id = restaurant["username"]
            goals = self.get_goals()
            rewards = self.get_rewards()
            board = restaurant["bingo_board"]

            board["board"] = [
                goal for index in board["board"] for goal in goals
                if index == goal["_id"]
            ]

            board["board_reward"] = [
                reward for index in board["board_reward"] for reward in rewards
                if index == reward["_id"]
            ]
            self.id = temp_id
            return board
        except (QueryFailureException, IndexError):
            print("Something's wrong with the query.")
            return {}
