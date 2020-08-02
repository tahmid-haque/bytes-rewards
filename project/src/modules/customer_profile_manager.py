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
