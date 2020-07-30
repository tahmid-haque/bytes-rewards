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

    def get_favourite(self, username):
        """
        Gets the list of user's favourite restaurant Ids
        """
        try: 
            customer = self.db.query("customers", {"username": self.id})[0]
            if "favourite" in customer:
                return customer["favourite"]
            else:
                return []
        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")

    def update_favourite(self, username, obj_id):
        """
        Updates the list of user's favourite restaurant Ids
        """
        try: 
            customer = self.db.query("customers", {"username": self.id})[0]
            if "favourite" not in customer:
                self.db.update("customers", {"username": self.id}, 
                    {"$push": 
                        {"favourite": 
                            ObjectId(obj_id)
                        }})
            else:
                if ObjectId(obj_id) in customer["favourite"]:
                    print("here")
                    self.db.update('customers', {"username": self.id},
                        {"$pull": {
                            "favourite": 
                                ObjectId(obj_id)
                        
                        }})
                else:
                    self.db.update('customers', {"username": self.id},
                        {"$push": {
                        "favourite": 
                            ObjectId(obj_id)
                   
                        }})
            return self.get_favourite(username)
        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")

    def get_favourite_doc(self, profiles, favourite):
        """
        Gets a dictionary of the user's favourite restaurant profiles
        """
        list_fav = {}
        for f in favourite:
            if f in profiles:
                list_fav[ObjectId(f)] = profiles[ObjectId(f)]
        return list_fav
			