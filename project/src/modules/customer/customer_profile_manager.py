"""
This file houses the customer profile management interface.
It is used to interact with the customer profile database.
"""
from modules.profile_manager import ProfileManager


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
