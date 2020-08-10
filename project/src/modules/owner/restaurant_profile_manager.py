"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""

from bson.objectid import ObjectId
from bson.errors import InvalidId
from modules.profile_manager import ProfileManager
from modules.database import Database, QueryFailureException


class RestaurantProfileManager(ProfileManager):
    """
    This class generates a restaurant profile manager, capable of managing
    one restaurant profile. It inherits from ProfileManager to perform basic
    creation/load operations.
    """

    @staticmethod
    def get_restaurant_name_by_id(object_id):
        """
        Given a restaurant user's database id, return the restaurant's name.
        Returns "" on failure.
        """
        try:
            db = Database.get_instance()
            user = db.query("restaurant_users", {"_id": ObjectId(object_id)})[0]
            return user["profile"]["name"]
        except (QueryFailureException, IndexError, KeyError, InvalidId):
            print("Something's wrong with the query.")
            return ""

    def __init__(self, username):
        """
        Initialize a restaurant user profile using the username.
        """
        ProfileManager.__init__(self, username, 'restaurant_users')

    def get_restaurant_id(self):
        """
        Return the restaurant ID of a restaurant user.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["_id"]
        except QueryFailureException:
            print("Something is wrong with the query")
            return []
