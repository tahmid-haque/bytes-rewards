"""
This file houses the customer profile management interface.
It is used to interact with the customer profile database.
"""
from bson.objectid import ObjectId
from modules.profile_manager import ProfileManager
from modules.database import QueryFailureException
from modules.restaurant_profile_manager import RestaurantProfileManager


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
        """
        Helper function to update a board with the customer's bingos.
        """
        ranges = [[4, 8, 12, 16, 20]]
        for i in range(0, 25, 5):
            ranges.append([x for x in range(i, i + 5)])
        for i in range(5):
            ranges.append([x for x in range(25) if x % 5 == i])
        ranges.append([0, 6, 12, 18, 24])

        count = 0
        for rang in ranges:
            is_bingo = True
            for i in rang:
                if i not in completed_indices:
                    is_bingo = False
            if is_bingo:
                for i in rang:
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

            # assign "not bingo" for all goals initially
            for i in range(len(board["board"])):
                board["board"][i]["is_bingo"] = False

            # assign "not earned" for all rewards initially
            for i in range(len(board["board_reward"])):
                board["board_reward"][i]["is_earned"] = False

            # assign complete for all goals the customer completed
            # assign bingo for all goals that make up a bingo that the customer completed
            # assign earned for all rewards that are earned
            customer = self.db.query("customers", {"username": self.id})[0]
            if "progress" in customer:
                for restaurant in customer["progress"]:
                    if restaurant["restaurant_id"] == rest_id:
                        for goal in restaurant["completed_goals"]:
                            completed_index = [
                                x["position"]
                                for x in restaurant["completed_goals"]
                            ]
                            index = int(goal["position"])
                            if board["board"][index]["_id"] == goal["_id"]:
                                board["board"][index]["is_complete"] = True
                                self.check_bingo(board, completed_index)

        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")

    def get_favourite(self):
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

    def update_favourite(self, obj_id):
        """
        Updates the list of user's favourite restaurant Ids
        """
        try:
            customer = self.db.query("customers", {"username": self.id})[0]
            if "favourite" not in customer:
                self.db.update("customers", {"username": self.id},
                               {"$push": {
                                   "favourite": ObjectId(obj_id)
                               }})
            else:
                if ObjectId(obj_id) in customer["favourite"]:
                    self.db.update('customers', {"username": self.id},
                                   {"$pull": {
                                       "favourite": ObjectId(obj_id)
                                   }})
                else:
                    self.db.update('customers', {"username": self.id},
                                   {"$push": {
                                       "favourite": ObjectId(obj_id)
                                   }})
            return self.get_favourite()
        except QueryFailureException:
            print("Something's wrong with the query.")
        except IndexError:
            print("Could not find the customer")

    def get_favourite_doc(self, profiles, favourite):
        """
        Gets a dictionary of the user's favourite restaurant profiles
        """
        list_fav = {}
        for fav in favourite:
            if fav in profiles:
                list_fav[ObjectId(fav)] = profiles[ObjectId(fav)]
        return list_fav

    def get_reward_progress(self):
        """
        Return the current user's reward history as a tuple of two lists:
        ([active rewards], [redeemed rewards]).
        Returns ([], []) on failure.
        """
        try:
            customer = self.db.query("customers", {"username": self.id})[0]

            # no game progress
            if "progress" not in customer:
                return ([], [])

            active_rewards = []
            redeemed_rewards = []
            for resaurant in customer["progress"]:

                # no rewards completed at this restaurant
                if "completed_rewards" not in resaurant:
                    continue

                restaurant_name = RestaurantProfileManager(
                    "").get_restaurant_name_by_id(resaurant["restaurant_id"])

                # add rewards to appropriate collection
                for reward in resaurant["completed_rewards"]:
                    reward["restaurant_name"] = restaurant_name
                    if reward["is_redeemed"]:
                        redeemed_rewards.append(reward)
                    else:
                        active_rewards.append(reward)

            # sort redeemed rewards by date
            redeemed_rewards = sorted(redeemed_rewards,
                                      key=lambda x: x["redemption_date"],
                                      reverse=True)

            # format all dates
            for index, reward in enumerate(redeemed_rewards):
                redeemed_rewards[index]["redemption_date"] = reward[
                    "redemption_date"].strftime("%B %d, %Y")

            return (active_rewards, redeemed_rewards)

        except QueryFailureException:
            print("Something's wrong with the query.")
            return ([], [])
        except IndexError:
            print("Could not find the customer")
            return ([], [])

    def update_board(self):
        """
        Checks all public restaurant user's bingo boards and replaces expired 
        boards with future game boards. If no future board exists, expiration
        date is increased by 90 days.
        """
        RestaurantProfileManager("").update_board()
