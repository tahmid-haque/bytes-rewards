from database import *

class restaurantProfileManager:

    def __init__(self, app, username):
        self.db = Database.get_instance(app)
        self.username = username

    def get_shared_goals(self):
        try:
            shared_goal_ids = self.db.query('goals', {"shared": True})[0]["goals"]
            return self.db.query('goals', {"_id" : {"$in" : shared_goal_ids}})
        except QueryFailureException:
            print("There was an issue retrieving goals.")
            return []

    def get_goals(self):
        return self.get_shared_goals()
    
    def get_bingo_board(self):
        try:
            rp = self.db.query('restaurant_users', {"username": self.username})
            return rp[0]["bingo_board"]
        except QueryFailureException:
            print("There was an issue retrieving a bingo board.")
            return {}
    
    def set_bingo_board(self, name, board):
        try:
            board = Database.replaceObjectID(board)

            self.db.update('restaurant_users', {"username": self.username}, {
                '$set': {
                    "bingo_board": {
                        "name": name,
                        "board": board
                    }
                }
            })
        except UpdateFailureException:
            print("There was an issue updating a bingo board.")