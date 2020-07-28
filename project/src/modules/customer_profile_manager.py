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

    def check_bingo(self, board, completed_indices): 
        ranges = [[4, 8, 12, 16, 20], [x for x in range(0,5)], [x for x in range(5,10)],
        [x for x in range(10,14)], [x for x in range(15,19)], [x for x in range(19,25)],
        [x for x in range(25) if x%5 == 0],[x for x in range(25) if x%5 == 1],
        [x for x in range(25) if x%5 == 2], [x for x in range(25) if x%5 == 3],
        [x for x in range(25) if x%5 == 4], [0, 6, 12, 18, 24]]
        
        count = 0
        for r in ranges:
            is_bingo = True
            for i in r:
                if i not in completed_indices:
                    is_bingo = False
            if is_bingo:
                for i in r:
                    board["board"][i]["is_bingo"] = True
                    board["board_reward"][count]["is_earned"] = True
            count += 1

    def set_board_progress(self, board, rest_id):
        """
        Given a board and restaurant id, update a board with the customer's progress.
        """
        try:
            rest_id = ObjectId(rest_id)

            # assign incomplete for all goals initially
            for i in range(len(board["board"])):
                board["board"][i]["is_complete"] = False
                
            for i in range(len(board["board"])):
                board["board"][i]["is_bingo"] = False
                
            for i in range(len(board["board_reward"])):
                board["board_reward"][i]["is_earned"] = False

            # assign complete for all goals the customer completed
            customer = self.db.query("customers", {"username": self.id})[0]
            if "progress" in customer:
                for restaurant in customer["progress"]:
                    if restaurant["restaurant_id"] == rest_id:
                        for goal in restaurant["completed_goals"]:
                            completed_indices = [x["position"] for x in restaurant["completed_goals"]]
                            index = int(goal["position"])
                            if board["board"][index]["_id"] == goal["_id"]:
                                board["board"][index]["is_complete"] = True
                                self.check_bingo(board, completed_indices)
            print(board["board_reward"])

        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")
