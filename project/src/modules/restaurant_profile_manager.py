"""
This file houses the restaurant profile management interface.
It is used to interact with the restaurant profile database.
"""

import copy
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from bson.errors import InvalidId
from modules.profile_manager import ProfileManager
from modules.database import Database, QueryFailureException, UpdateFailureException


class RestaurantProfileManager(ProfileManager):
    """
    This class generates a restaurant profile manager, capable of managing
    one restaurant profile. Some of the things it manages include goals and
    bingo boards. It inherits from ProfileManager to perform basic
    creation/load operations.
    """

    def __init__(self, username):
        """
        Initialize a restaurant user profile using the username.
        """
        ProfileManager.__init__(self, username, 'restaurant_users')

    def get_shared_goals(self):
        """
        Return a list of all goals that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.db.query('goals')
        except QueryFailureException:
            print("There was an issue retrieving goals.")
            return []

    def get_goals(self):
        """
        Return a list of all goals that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_goals()
        shared = self.get_shared_goals()
        return custom + shared

    def get_bingo_board(self):
        """
        Return the active bingo board attached to the current restaurant user.
        """
        try:
            profile = self.db.query('restaurant_users', {"username": self.id})
            return profile[0]["bingo_board"]
        except KeyError:  # New User, no bingo board found
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }
        except (QueryFailureException, IndexError):
            print("There was an issue retrieving a bingo board.")
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }

    def set_bingo_board(self, bingo_board):
        """
        Update the restaurant user's bingo board using the board.
        """
        try:
            # convert the date string to a python date
            if not isinstance(bingo_board["expiry_date"], datetime):
                date = [
                    int(part) for part in bingo_board["expiry_date"].split("/")
                ]
                bingo_board["expiry_date"] = datetime(date[2], date[0], date[1],
                                                      23, 59, 59)

            # convert ids to object ids
            bingo_board["board"] = Database.replace_object_id(
                bingo_board["board"])
            bingo_board["board_reward"] = Database.replace_object_id(
                bingo_board["board_reward"])

            # if new user, update current board as well as future board
            boards = {"future_board": bingo_board}
            if self.get_future_board()["name"] == "":
                boards["bingo_board"] = copy.deepcopy(bingo_board)
                boards["future_board"]["expiry_date"] = boards["future_board"]["expiry_date"] + \
                                                        timedelta(days=90)

            self.db.update('restaurant_users', {"username": self.id},
                           {'$set': boards})
        except (UpdateFailureException, KeyError):
            print("There was an issue updating a bingo board.")

    def get_shared_rewards(self):
        """
        Return a list of all rewards that are shared among all restaurant
        profiles. This includes the curated list of goals created by the
        Bytes team.
        """
        try:
            return self.db.query('rewards')
        except QueryFailureException:
            print("There was an issue retrieving rewards.")
            return []

    def get_rewards(self):
        """
        Return a list of all rewards that the current restaurant user can use
        within their profile.
        """
        custom = self.get_custom_rewards()
        shared = self.get_shared_rewards()
        return custom + shared

    def get_profile(self):
        """
        Return the restaurant user's profile.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
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
            self.db.update('restaurant_users', {"username": self.id},
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
            restaurant_owners = self.db.query('restaurant_users',
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

    def get_custom_goals(self):
        """
        Gets custom goals added by the user.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["goals"]
        except KeyError:  # New User, no goals found
            return []
        except (QueryFailureException, IndexError):
            print("Something is wrong with the query")
            return []

    def add_custom_goal(self, goal):
        """
        Add a custom goal to the restaurant profile. If successful, return True.
        If goal already exists, return False.
        """
        goals = self.get_goals()
        in_database = [x['goal'] for x in goals if x['goal'] == goal]
        if in_database == []:
            try:
                self.db.update(
                    'restaurant_users', {"username": self.id},
                    {"$push": {
                        "goals": {
                            "_id": ObjectId(),
                            "goal": goal
                        }
                    }})
                return True
            except UpdateFailureException:
                print("There was an issue updating the goals")
                return False
        return False

    def remove_custom_goal(self, goal_id):
        """
        Remove a restaurant user's custom goal from their database and returns
        "current" if the goal is on the current board, "future" if it is on
        the future board, "success" upon sucessful deletion, otherwise "fail"
        and throws an exception.
        """
        try:
            goals = self.get_bingo_board()["board"]
            future_goals = self.get_future_board()["board"]
            if ObjectId(goal_id) in goals:
                return "current"
            elif ObjectId(goal_id) in future_goals:
                return "future"
            self.db.update('restaurant_users', {"username": self.id},
                           {"$pull": {
                               "goals": {
                                   "_id": ObjectId(goal_id)
                               }
                           }})
            return "sucess"
        except QueryFailureException:
            print("There was an issue deleting the goal.")
            return "fail"

    def add_custom_reward(self, reward):
        """
        Add a custom reward to the restaurant profile. If successful, return True.
        If reward already exists, return False.
        """
        try:
            rewards = self.get_rewards()
            in_database = [
                x['reward'] for x in rewards if x['reward'] == reward
            ]
            if in_database == []:
                try:
                    self.db.update('restaurant_users', {"username": self.id}, {
                        "$push": {
                            "rewards": {
                                "_id": ObjectId(),
                                "reward": reward
                            }
                        }
                    })
                    return True
                except UpdateFailureException:
                    print("There was an issue updating the rewards")
                    return False
        except QueryFailureException:
            print("Something is wrong with the query")
            return False
        return False

    def get_custom_rewards(self):
        """
        Gets custom rewards added by the user.
        """
        try:
            user = self.db.query('restaurant_users', {"username": self.id})[0]
            return user["rewards"]
        except KeyError:  # New User, no rewards found
            return []
        except QueryFailureException:
            print("Something is wrong with the query")
            return []

    def remove_custom_reward(self, reward_id):
        """
        Remove a restaurant user's custom reward that is not on their game board
        from their database and and returns
        "current" if the goal is on the current board, "future" if it is on
        the future board, "success" upon sucessful deletion, otherwise "fail"
        and throws an exception.
        """
        try:
            rewards = self.get_bingo_board()["board_reward"]
            future_rewards = self.get_future_board()["board_reward"]
            if ObjectId(reward_id) in rewards:
                return "current"
            elif ObjectId(reward_id) in future_rewards:
                return "future"
            self.db.update('restaurant_users', {"username": self.id},
                           {"$pull": {
                               "rewards": {
                                   "_id": ObjectId(reward_id)
                               }
                           }})
            return "success"
        except QueryFailureException:
            print("There was an issue deleting the reward.")
            return "fail"

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

    def get_restaurant_board_by_id(self, rest_id):
        """
        Return a restaurant board given a restaurant database id. The board will include
        text info for goals and rewards.
        """
        try:
            temp_id = self.id
            restaurant = self.db.query("restaurant_users",
                                       {"_id": ObjectId(rest_id)})[0]
            self.id = restaurant["username"]
            goals = self.get_goals()
            rewards = self.get_rewards()
            board = restaurant["bingo_board"]

            board["board"] = [
                copy.deepcopy(goal)
                for index in board["board"]
                for goal in goals
                if index == goal["_id"]
            ]

            board["board_reward"] = [
                copy.deepcopy(reward)
                for index in board["board_reward"]
                for reward in rewards
                if index == reward["_id"]
            ]
            self.id = temp_id
            return board
        except (QueryFailureException, IndexError):
            print("Something's wrong with the query.")
            return {}

    def get_restaurant_profile_by_id(self, rest_id):
        """
        Return a restaurant profile given a restaurant database id.
        """
        try:
            restaurant = self.db.query("restaurant_users",
                                       {"_id": ObjectId(rest_id)})[0]
            return restaurant["profile"]
        except (QueryFailureException, IndexError, KeyError):
            print("There was an issue retrieving the profile.")
            return {}

    def add_reward_code(self, customer, reward_index):
        """
        Adds a reward code to the databases if there is a bingo on the board
        """
        owner = self.db.query('restaurant_users', {"username": self.id})[0]
        reward_id = owner["bingo_board"]["board_reward"][reward_index]
        rewards = self.get_rewards()
        text = ""
        for reward in rewards:
            if str(reward["_id"]) == str(reward_id):
                text = reward["reward"]
        customer_profile = self.db.query('customers', {"username": customer})[0]
        code = str(customer) + "+" + str(reward_id) + "+" + str(reward_index) + "+" + str(datetime.now())
        try:
            if "client_rewards" not in owner:
                self.db.update('restaurant_users', {"username": self.id},
                               {"$set": {
                                   "client_rewards": [{
                                       "redemption_code": code,
                                       "text": text,
                                       "is_redeemed": False
                                   }]
                               }})
            else:
                self.db.update('restaurant_users', {"username": self.id},
                               {"$push": {
                                   "client_rewards": {
                                       "redemption_code": code,
                                       "text": text,
                                       "is_redeemed": False
                                   }
                               }})
        except UpdateFailureException:
            print("There was an issue updating")

        try:
            self.db.update('customers', {"username": customer, "progress.restaurant_id": ObjectId(str(owner["_id"]))},
                           {"$push": {
                               "progress.$.completed_rewards": {
                                   "redemption_code": code,
                                   "text": text,
                                   "is_redeemed": False
                               }
                           }})
        except UpdateFailureException:
            print("There was an issue updating")
            return "Error"

    def check_row(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the rows
        """
        start = int(position)
        counter = 0
        while (start % size) != 0:
            start = start - 1
        for i in range(start, start + size):
            for goal in goals:
                if i == int(goal["position"]):
                    counter = counter + 1
        if counter == size:
            self.add_reward_code(customer, int(int(position) / size) + 1)

    def check_col(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the columns
        """
        start = int(position)
        counter = 0
        while (start - size) > 0:
            start = start - size
        for i in range(start, size * size, size):
            for goal in goals:
                if i == int(goal["position"]):
                    counter = counter + 1
        if counter == size:
            self.add_reward_code(customer, ((int(position) + 1) % size) + 5)

    def check_diagonal(self, position, size, customer, goals):
        """
        Checks if there is a bingo on the diagonals
        """
        left = False
        right = False
        counter = 0
        start = int(position)
        while start >= 0:
            if start == 0:
                left = True
            start = start - (size + 1)

        start = int(position)
        while start >= (size - 1):
            if start == (size - 1):
                right = True
            start = start - (size - 1)

        if left:
            for i in range(0, size * size, size + 1):
                for goal in goals:
                    if i == int(goal["position"]):
                        counter = counter + 1
            if counter == size:
                self.add_reward_code(customer, size + size + 1)
        counter = 0
        if right:
            for i in range(size - 1, (size * size - (size - 1)), size - 1):
                for goal in goals:
                    if i == int(goal["position"]):
                        counter = counter + 1
                i = i + size - 1
            if counter == size:
                self.add_reward_code(customer, 0)

    def complete_goal(self, user, goal_id, position):
        """
        Adds a goal to the database that has been completed by the customer and returns
        a message depending on if it is successful or not.
        """
        try:
            owner_id = self.db.query('restaurant_users', {"username": self.id})[0]["_id"]
            size = self.db.query('restaurant_users', {"username": self.id})[0]["bingo_board"]["size"]
            user_profile = self.db.query('customers', {"username": user})[0]
            goals = []
            if "progress" in user_profile:
                for restaurant in user_profile["progress"]:
                    if restaurant["restaurant_id"] == owner_id:
                        goals = restaurant["completed_goals"]
                        for goal in goals:
                            if str(goal["_id"]
                                   ) == goal_id and position == goal["position"]:
                                return "This goal has already been completed!"
                        id_exists = True
            if not isinstance(int(position), int) or \
                    not (1 <= len(position) <= 2) or not (0 <= int(position) <= 24) or \
                    not str(self.get_bingo_board()["board"][int(position)]) == goal_id:
                return "Invalid QR code!"
            try:
                if "progress" in user_profile and id_exists:
                    self.db.update(
                        'customers', {
                            "username": user,
                            "progress.restaurant_id": ObjectId(owner_id)
                        }, {
                            "$push": {
                                "progress.$.completed_goals": {
                                    "_id": ObjectId(goal_id),
                                    "position": position,
                                    "date_completed": datetime.now()
                                }
                            }
                        })
                else:
                    self.db.update('customers', {"username": self.id}, {
                        "$push": {
                            "progress": {
                                "restaurant_id":
                                    ObjectId(owner_id),
                                "completed_goals": [{
                                    "_id": ObjectId(goal_id),
                                    "position": position,
                                    "date": datetime.now()
                                }],
                                "completed_rewards": []
                            }
                        }
                    })
                user_profile = self.db.query('customers', {"username": user})[0]
                for restaurant in user_profile["progress"]:
                    if restaurant["restaurant_id"] == owner_id:
                        goals = restaurant["completed_goals"]
                self.check_col(position, size, user, goals)
                self.check_diagonal(position, size, user, goals)
                self.check_row(position, size, user, goals)
                return "Successfully marked as completed!"
            except UpdateFailureException:
                print("There was an issue updating")
                return "Error"
        except QueryFailureException:
            print("Something is wrong with the query")
            return "Error"
        return "Error"

    def get_restaurant_name_by_id(self, object_id):
        """
        Given a restaurant user's database id, return the restaurant's name.
        Returns "" on failure.
        """
        try:
            user = self.db.query("restaurant_users",
                                 {"_id": ObjectId(object_id)})[0]
            return user["profile"]["name"]
        except (QueryFailureException, IndexError, KeyError, InvalidId):
            print("Something's wrong with the query.")
            return ""

    def update_board(self, id):
        """
        Checks all public restaurant user's bingo boards and replaces expired
        boards with future game boards. If no future board exists, expiration
        date is increased by 90 days.
        """
        try:
            user = self.db.query('restaurant_users', {'_id': id})
            reset = 90  # expiration date deafault is set to 90 days
            if 'expiry_date' in user[0]['bingo_board']:
                if datetime.now() >= user[0]['bingo_board'][
                    'expiry_date']:  # expired current board
                    if 'future_board' in user[0]:
                        future_exp = user[0]['future_board']['expiry_date']
                        if future_exp <= datetime.now():  # expired future goal
                            future_exp = datetime.now() + timedelta(days=reset)
                        user[0]['future_board'][
                            'expiry_date'] = future_exp  # updates future exp date
                        self.db.update(  # updates current board in db
                            'restaurant_users',
                            {'username': user[0]['username']},
                            {'$set': {
                                'bingo_board': user[0]['future_board']
                            }})
                        user[0]['future_board'][  # updates future board in db
                            'expiry_date'] = future_exp + timedelta(days=reset)
                        self.db.update(
                            'restaurant_users',
                            {'username': user[0]['username']},
                            {'$set': {
                                'future_board': user[0]['future_board']
                            }})
                    customers = self.db.query('customers')
                    for c in customers:
                        if 'progress' in c:
                            for item in c['progress']:
                                # checks for completed goals corresponding to expired board
                                if item['restaurant_id'] == ObjectId(
                                        id) and 'completed_goals' in item:
                                    self.db.update(  # removes current goals in customer profiles
                                        'customers', {
                                            "username": c['username'],
                                            "progress.restaurant_id": id
                                        }, {
                                            "$set": {
                                                "progress.$.completed_goals": [
                                                ]
                                            }
                                        })
        except UpdateFailureException:
            print("There was an issue updating")
        except KeyError:
            print("No current board")

    def get_future_board(self):
        """
        Return the future board attached to the current restaurant user.
        """
        try:
            profile = self.db.query('restaurant_users', {"username": self.id})
            return profile[0]["future_board"]
        except KeyError:  # New User, no future board found
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }
        except (QueryFailureException, IndexError):
            print("There was an issue retrieving a bingo board.")
            return {
                "name": "",
                "board": [],
                "board_reward": [],
                "expiry_date": None,
                "size": 4
            }

    def get_current_board_expiry(self):
        """
        Return the expiry date of the user's active board.
        """
        try:
            profile = self.db.query('restaurant_users', {"username": self.id})
            return profile[0]["bingo_board"]["expiry_date"]
        except (QueryFailureException, IndexError, KeyError, InvalidId):
            return None

    def complete_reward(self, user, code):
        """
        Adds a reward to the database that has been completed by the customer and returns
        a message depending on if it is successful or not.
        """
        try:
            owner = self.db.query('restaurant_users', {"username": self.id})[0]
            user_profile = self.db.query('customers', {"username": user})[0]
            in_user = False
            counter = -1
            if "progress" in user_profile:
                for restaurant in user_profile["progress"]:
                    counter += 1
                    if restaurant["restaurant_id"] == owner["_id"]:
                        restaurant_index = counter
                        rewards = restaurant['completed_rewards']
                        counter = -1
                        for reward in rewards:
                            counter += 1
                            if reward["redemption_code"] == code:
                                text = reward["text"]
                                in_user = True
                                customer_index = counter
                                if "redemption_date" in reward:
                                    return "Code has already been redeemed!"
                if not in_user:
                    return "Invalid QR code!"
            counter = -1
            for reward in owner["client_rewards"]:
                counter += 1
                if reward["redemption_code"] == code:
                    owner_index = counter

            self.db.update('restaurant_users', {"username": self.id, "client_rewards.redemption_code": code},
                           {"$set": {
                               "client_rewards." + str(owner_index): {
                                   "redemption_code": code,
                                   "text": text,
                                   "is_redeemed": True,
                                   "redemption_date": datetime.now()
                               }
                           }})

            self.db.update('customers', {"username": user, "progress.restaurant_id": ObjectId(str(owner["_id"])),
                                         "progress.completed_rewards.redemption_code": code},
                           {"$set": {
                               "progress." + str(restaurant_index) + ".completed_rewards." + str(customer_index): {
                                   "redemption_code": code,
                                   "text": text,
                                   "is_redeemed": True,
                                   "redemption_date": datetime.now()
                               }
                           }})

            return "Successfully marked as completed!"
        except QueryFailureException:
            print("Something is wrong with the query")
            return "Error"
        return "Error"
