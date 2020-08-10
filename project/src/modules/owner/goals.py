"""
This file houses the goal management interface for restaurant users.
It is used to interact with the goals database and manipulate custom goals for
restaurant users.
"""
from bson.objectid import ObjectId
from modules.database import QueryFailureException, UpdateFailureException
from modules.owner.game_board import GameBoardManager


class GoalsManager:
    """
    This class generates a goals manager capable of retrieving goals from the goals
    database and also manipulating custom goals for restaurant users.
    """

    def __init__(self, restaurant_profile_manager):
        """
        Initialize a goals manager using the provided restaurant profile manager.
        """
        self.rpm = restaurant_profile_manager

    def get_shared_goals(self):
        """
        Return a list of all goals that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.rpm.db.query('goals')
        except QueryFailureException:
            print("There was an issue retrieving goals.")
            return []

    def get_custom_goals(self):
        """
        Gets custom goals added by the user.
        """
        try:
            user = self.rpm.db.query('restaurant_users',
                                     {"username": self.rpm.get_id()})[0]
            return user["goals"]
        except KeyError:  # New User, no goals found
            return []
        except (QueryFailureException, IndexError):
            print("Something is wrong with the query")
            return []

    def get_goals(self):
        """
        Return a list of all goals that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_goals()
        shared = self.get_shared_goals()
        return custom + shared

    def add_custom_goal(self, goal):
        """
        Add a custom goal to the restaurant profile. If successful, return True.
        If goal already exists, return False.
        """
        goals = self.get_goals()
        in_database = [x['goal'] for x in goals if x['goal'] == goal]
        if in_database == []:
            try:
                self.rpm.db.update(
                    'restaurant_users', {"username": self.rpm.get_id()},
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
        "current" if the goal is on the current board, "future" if it is on
        the future board, "success" upon sucessful deletion, otherwise "fail"
        and throws an exception.
        """
        try:
            gbm = GameBoardManager(self.rpm)

            goals = gbm.get_bingo_board()["board"]
            future_goals = gbm.get_future_board()["board"]
            if ObjectId(goal_id) in goals:
                return "current"
            if ObjectId(goal_id) in future_goals:
                return "future"
            self.rpm.db.update('restaurant_users',
                               {"username": self.rpm.get_id()},
                               {"$pull": {
                                   "goals": {
                                       "_id": ObjectId(goal_id)
                                   }
                               }})
            return "sucess"
        except QueryFailureException:
            print("There was an issue deleting the goal.")
            return "fail"
