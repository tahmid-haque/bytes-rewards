"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""

from bson.objectid import ObjectId
from modules.profile_manager import ProfileManager
from modules.database import Database, QueryFailureException, UpdateFailureException
from datetime import datetime

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
        return custom+shared

    def get_bingo_board(self):
        """
        Return a bingo board attached to the current restaurant user.
        """
        try:
            profile = self.db.query('restaurant_users', {"username": self.id})
            return profile[0]["bingo_board"]
        except KeyError:  # New User, no bingo board found
            return {"name": "", "board": [], "board_reward": []}
        except QueryFailureException:
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
        Return a list of all goals that the curren  t restaurant user can use
        within their profile.
        """
        return self.get_shared_rewards()

    def get_profile(self):
        """
        Return the restaurant user's profile.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["profile"]
        except KeyError:  # New User, no profile found
            return {}
        except QueryFailureException:
            print("There was an issue retrieving a profile")
            return {}

    def update_profile(self, profile):
        """
        Update the restaurant user's profile using the data provided in profile.
        """
        profile['is_public'] = 'is_public' in profile
        try:
            self.db.update('restaurant_users', {"username": self.id}, {
                '$set': {
                    "profile": profile
                }
            })
        except UpdateFailureException:
            print("There was an issue updating a profile.")

    def get_public_users(self):
        """
        Get all restaurant users that have a public profile.
        """
        try:
            restaurant_owners = self.db.query('restaurant_users', {
                'profile.is_public': True
            })
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
        except QueryFailureException:
            print("Something is wrong with the query")
            return []

    def add_custom_goal(self, goal):
        """
        Add a custom goal to the restaurant profile. If successful, return True.
        If goal already exists, return False.
        """
        try:
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
        except QueryFailureException:
            print("Something is wrong with the query")
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
            self.db.update('restaurant_users', {"username": self.id}, {
                "$pull": {
                    "goals": {
                        "_id": ObjectId(goal_id)
                    }
                }
            })
            return True
        except QueryFailureException:
            print("There was an issue deleting the goal.")
            return False


    def complete_goal(self, user, goal_id, position):
        """
        Adds a goal to the database that has been completed by the customer and returns
        a message depending on if it is successful or not.
        """
        try:
            owner_id = self.db.query('restaurant_users', {"username": self.id})[0]["_id"]
            user_profile = self.db.query('customers', {"username": user})[0]
            if "progress" in user_profile:
                for restaurant in user_profile["progress"]:
                    if restaurant["restaurant_id"] == owner_id:
                        goals = restaurant["completed_goals"]
                        for goal in goals:
                            if str(goal["_id"]) == goal_id and position == goal["position"]:
                                return "This goal has already been completed!"
                        id_exists = True
            if not isinstance(int(position), int) or not (1 <= len(position) <= 2) or not (0 <= int(position) <= 24) \
                    or not str(self.get_bingo_board()["board"][int(position)]) == goal_id:
                return "Invalid QR code!"
            try:
                if "progress" in user_profile and id_exists:
                    self.db.update('customers', {"username": user, "progress.restaurant_id": ObjectId(owner_id)},
                                   {"$push": {
                                       "progress.$.completed_goals": {
                                           "_id": ObjectId(goal_id),
                                           "position": position,
                                           "date_completed": datetime.now()}}})
                else:
                    self.db.update(
                        'customers', {"username": self.id},
                        {"$push": {
                            "progress": {
                                "restaurant_id": ObjectId(owner_id),
                                "completed_goals": [{
                                    "_id": ObjectId(goal_id),
                                    "position": position,
                                    "date": datetime.now()
                                }]
                            }
                        }})
                return "Successfully marked as completed!"
            except UpdateFailureException:
                print("There was an issue updating")
                return "Error"
        except QueryFailureException:
            print("Something is wrong with the query")
            return "Error"
        return "Error"
