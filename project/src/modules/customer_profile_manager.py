"""
This file houses the customer profile management interface.
It is used to interact with the customer profile database.
"""
from modules.profile_manager import ProfileManager
from modules.database import QueryFailureException


class CustomerProfileManager(ProfileManager):
    """
    This class generates a customer profile manager, capable of managing
    one customer profile. Some of the things it manages include goals and
    bingo boards. It inherits from ProfileManager to perform basic
    creation/load operations.
    """

    def __init__(self, username):
        """
        Initialize a customer profile using the current app and username
        """
        ProfileManager.__init__(self, username, 'customers')

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
