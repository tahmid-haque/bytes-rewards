"""
This file houses the restaurant profile's public profile modifier.
It is used to interact with a restaurant owner's restaurant information.
"""
from bson.objectid import ObjectId
from modules.database import QueryFailureException, UpdateFailureException


class PublicProfileModifier():
    """
    This class generates a public profile modifier capable of managing a restaurant
    owner's profile information. This is the data that customers see when they look at
    a public restaurant profile.
    """

    def __init__(self, restaurant_profile_manager):
        """
        Initialize a public profile modifier using the given restaurant profile manager.
        """
        self.rpm = restaurant_profile_manager

    def get_profile(self):
        """
        Return the restaurant user's profile.
        """
        try:
            user = self.rpm.db.query('restaurant_users',
                                     {"username": self.rpm.get_id()})[0]
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
            self.rpm.db.update('restaurant_users',
                               {"username": self.rpm.get_id()},
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
            restaurant_owners = self.rpm.db.query('restaurant_users',
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

    def get_restaurant_profile_by_id(self, rest_id):
        """
        Return a restaurant profile given a restaurant database id.
        """
        try:
            restaurant = self.rpm.db.query("restaurant_users",
                                           {"_id": ObjectId(rest_id)})[0]
            return restaurant["profile"]
        except (QueryFailureException, IndexError, KeyError):
            print("There was an issue retrieving the profile.")
            return {}
