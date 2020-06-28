"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""

from database import Database, QueryFailureException, UpdateFailureException


class RestaurantProfileManager:
    """
    This class generates a restaurant profile manager, capable of managing
    one restaurant profile. Some of the things it manages include goals and
    bingo boards.
    """

    def __init__(self, app, username):
        """
        Initialize the database object using the flask app.
        """
        self.db = Database.get_instance(app)
        self.username = username

    def get_shared_goals(self):
        """
        Return a list of all goals that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            shared_goal_ids = self.db.query('goals',
                                            {"shared": True})[0]["goals"]
            return self.db.query('goals', {"_id": {"$in": shared_goal_ids}})
        except QueryFailureException:
            print("There was an issue retrieving goals.")
            return []

    def get_goals(self):
        """
        Return a list of all goals that the current restaurant user can use
        within their profile.
        """
        return self.get_shared_goals()

    def get_bingo_board(self):
        """
        Return a bingo board attached to the current restaurant user.
        """
        try:
            profile = self.db.query('restaurant_users',
                                    {"username": self.username})
            return profile[0]["bingo_board"]
        except QueryFailureException:
            print("There was an issue retrieving a bingo board.")
            return {}

    def set_bingo_board(self, name, board):
        """
        Update the restaurant user's bingo board using the given name and
        board.
        """
        try:
            board = Database.replace_object_id(board)

            self.db.update(
                'restaurant_users', {"username": self.username},
                {'$set': {
                    "bingo_board": {
                        "name": name,
                        "board": board
                    }
                }})
        except UpdateFailureException:
            print("There was an issue updating a bingo board.")
