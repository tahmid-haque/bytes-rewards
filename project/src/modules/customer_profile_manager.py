"""
This file houses the customer profile management interface.
It is used to interact with the customer profile database.
"""
from bson.objectid import ObjectId
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

    def set_board_progress(self, board, rest_id):
        """
        Given a board and restaurant id, update a board with the customer's progress.
        """
        try:
            rest_id = ObjectId(rest_id)

            # assign incomplete for all goals initially
            for i in range(len(board["board"])):
                board["board"][i]["is_complete"] = False

            # assign complete for all goals the customer completed
            customer = self.db.query("customers", {"username": self.id})[0]
            if "progress" in customer:
                for restaurant in customer["progress"]:
                    if restaurant["restaurant_id"] == rest_id:
                        for goal in restaurant["completed_goals"]:
                            index = int(goal["position"])
                            if board["board"][index]["_id"] == goal["_id"]:
                                board["board"][index]["is_complete"] = True

        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")
