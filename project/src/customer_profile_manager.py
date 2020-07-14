"""
This file houses the customer profile management interface.
It is used to interact with the customer profile database.
"""
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database, QueryFailureException, InsertFailureException


class CustomerProfileManager(UserMixin):
    """
    This class generates a customer profile manager, capable of managing
    one customer profile. Some of the things it manages include goals and
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

    def set_new_profile(self, fullname, password):
        """
        Create a new profile in the database given the credentials of this
        instance.
        """
        try:
            self.hashed_pw = generate_password_hash(password, method='sha256')
            self.fullname = fullname
            self.db.insert(
                'customers', {
                    "fullname": fullname,
                    "username": self.username,
                    "hashed_password": self.hashed_pw
                })
            return "Profile set successfully."
        except InsertFailureException:
            return "There was an issue creating a new user profile."

    def check_user_exists(self, username):
        """
        Return True if the user exists in the database, else throw an exception.
        """
        try:
            customer_user = self.db.query('customers', {'username': username})
            return len(customer_user) != 0
        except QueryFailureException:
            print("Something's wrong with the query.")

    def get_user(self):
        """
        Update an instance to fully represent a user.
        """
        try:
            customer_user = self.db.query('customers',
                                          {'username': self.username})
            if len(customer_user) > 0:
                self.fullname = customer_user[0]['fullname']
                self.hashed_pw = customer_user[0]['hashed_password']
            return "Got user successfully."
        except QueryFailureException:
            return "There was an issue retrieving user credentials."

    def get_goals(self):
        """
        Get all goals from database
        """
        try:
            goals = self.db.query('goals')
            return goals
        except QueryFailureException:
            print("Something's wrong with the query.")
            return []

    def get_rewards(self):
        """
        Get all rewards from database
        """
        try:
            goals = self.db.query('rewards')
            return goals
        except QueryFailureException:
            print("Something's wrong with the query.")
            return []

    def get_restaurant_profiles(self):
        """
        Get all restaurant profiles that are ready to be viewed.
        """
        try:
            restaurant_owners = self.db.query('restaurant_users',
                                              {'profile.is_public': True})
            return {
                owner["_id"]: owner["profile"] for owner in restaurant_owners
            }
        except QueryFailureException:
            print("Something's wrong with the query.")
            return []

    def get_restaurant_users(self):
        """
        Get all restaurant profiles that are ready to be viewed.
        """
        try:
            restaurant_owners = self.db.query('restaurant_users',
                                              {'profile.is_public': True})
            return restaurant_owners
        except QueryFailureException:
            print("Something's wrong with the query.")
            return []
