"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database, QueryFailureException, UpdateFailureException, InsertFailureException


class RestaurantProfileManager(UserMixin):
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
        self.id = u""  # Overwritten by get_id()
        self.fullname = ""
        self.username = username
        self.hashed_pw = ""

    def check_password(self, password):
        """
        Check if given password matches hash.
        """
        return check_password_hash(self.hashed_pw, password)

    def set_new_profile(self, fullname, username, password):
        """
        Create a new profile in the database given the credentials of this instance.
        """
        try:
            self.hashed_pw = generate_password_hash(password, method='sha256')
            self.fullname = fullname
            self.db.insert(
                'restaurant_users', {
                    "fullname": fullname,
                    "username": username,
                    "hashed_password": self.hashed_pw
                })
        except InsertFailureException:
            return "There was an issue creating a new user profile."

    def check_user_exists(self, username):
        """
        Return True if the user exists in the database.
        """
        try:
            restaurant_user = self.db.query('restaurant_users',
                                            {'username': username})
            return len(restaurant_user) != 0
        except QueryFailureException:
            print("Something's wrong with the query.")

    def get_user(self, username):
        """
        Update an instance to fully represent a user.
        """
        try:
            restaurant_user = self.db.query('restaurant_users',
                                            {'username': username})
            if len(restaurant_user) > 0:
                self.fullname = restaurant_user[0]['fullname']
                self.username = username
                self.hashed_pw = restaurant_user[0]['hashed_password']
        except QueryFailureException:
            return "There was an issue retrieving user credentials."

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
            if len(profile) == 0:  # Nothing was queried for some reason.
                print(
                    "Something's wrong with Victor. He's not being queried properly. TODO"
                )
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
