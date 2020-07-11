"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""
# Import flask_login's base User class for proper integration
from flask_login import UserMixin
# Import for secure password storage
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database, QueryFailureException, UpdateFailureException, InsertFailureException


class RestaurantProfileManager(UserMixin):
    """
    This class generates a restaurant profile manager, capable of managing
    one restaurant profile. Some of the things it manages include goals and
    bingo boards. It inherits from UserMixin to properly integrate with the
    features of flask_login.
    """
    def __init__(self, app, username):
        """
        Initialize the database object using the flask app.
        """
        self.db = Database.get_instance(app)
        self.fullname = ""
        self.username = username
        self.hashed_pw = ""

    def check_password(self, password):
        """
        Check if given password matches hash.
        """
        return check_password_hash(self.hashed_pw, password)

    def set_new_profile(self, fullname, password):
        """
        Create a new profile in the database given the credentials of this instance.
        If unable to insert, throws InsertFailureException.
        """
        try:
            self.hashed_pw = generate_password_hash(password, method='sha256')
            self.fullname = fullname
            self.db.insert(
                'restaurant_users', {
                    "fullname": fullname,
                    "username": self.username,
                    "hashed_password": self.hashed_pw,
                    "restaurant_name": "",
                    "categories": [],
                    "image_url": "",
                    "description": "",
                    "phone_num": "",
                    "address": "",
                    "goals": [],
                    "rewards": [],
                    "bingo_board": {
                        "name":"",
                        "board":[]
                    },
                    "ready_to_view": False
                })
        except InsertFailureException:
            print("There was an issue creating a new user profile.")

    def check_user_exists(self, username):
        """
        Return True if the user exists in the database.
        If there is an issue with the query, throws QueryFailureException.
        """
        try:
            restaurant_user = self.db.query('restaurant_users',
                                            {'username': username})
            return len(restaurant_user) != 0
        except QueryFailureException:
            print("Something's wrong with the query.")

    def get_user(self):
        """
        Update an instance to fully represent a user.
        If there is an issue with the query, throws QueryFailureException.
        """
        try:
            restaurant_user = self.db.query('restaurant_users',
                                            {'username': self.username})
            if len(restaurant_user) > 0:
                self.fullname = restaurant_user[0]['fullname']
                self.hashed_pw = restaurant_user[0]['hashed_password']
        except QueryFailureException:
            print("There was an issue retrieving user credentials.")

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
                    "Goes into this block. TODO"
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

    def get_id(self):
        """
        Retrieves the username for flask-login.
        """
        return self.username

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
            self.db.update('restaurant_users', {"username": self.id},
                           {'$set': {
                               "profile": profile
                           }})
        except UpdateFailureException:
            print("There was an issue updating a profile.")
