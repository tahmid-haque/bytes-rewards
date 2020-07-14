"""
This file contains a generic profile manager that performs basic profile handling.
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from modules.database import Database, QueryFailureException, InsertFailureException


class ProfileManager(UserMixin):
    """
    This class handles the loading, creation of user profiles. It inherits from UserMixin
    to properly integrate with the features of flask_login.
    """

    def __init__(self, username, collection):
        """
        Initialize a profile using the username, app instance and database collection.
        """
        self.db = Database.get_instance()
        self.id = username.lower()
        self.fullname = ""
        self.hashed_pw = ""
        self.database_collection = collection

    def check_password(self, password):
        """
        Check if given password matches hash.
        """
        return check_password_hash(self.hashed_pw, password)

    def set_new_profile(self, fullname, password):
        """
        Create a new profile in the database given the credentials of this
        instance.
        """
        try:
            self.hashed_pw = generate_password_hash(password, method='sha256')
            self.fullname = fullname
            self.db.insert(
                self.database_collection, {
                    "fullname": fullname,
                    "username": self.id,
                    "hashed_password": self.hashed_pw
                })
            return "Profile set successfully."
        except InsertFailureException:
            return "There was an issue creating a new user profile."

    def check_user_exists(self):
        """
        Return True if the user exists in the database, else throw an exception.
        """
        try:
            user = self.db.query(self.database_collection,
                                 {'username': self.id})
            return len(user) != 0
        except QueryFailureException:
            print("Something's wrong with the query.")

    def get_user(self):
        """
        Update an instance to fully represent a user.
        """
        try:
            user = self.db.query(self.database_collection,
                                 {'username': self.id})
            if len(user) > 0:
                self.fullname = user[0]['fullname']
                self.hashed_pw = user[0]['hashed_password']
            return "Got user successfully."
        except QueryFailureException:
            return "There was an issue retrieving user credentials."
