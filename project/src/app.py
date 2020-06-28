"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""
import os
from flask import Flask, render_template, request, redirect
from restaurant_profile_manager import RestaurantProfileManager

app = Flask(__name__)  # Initialize a flask app using current file


@app.route('/')
def index():
    """
    When retrieving this route, get a restaurant profile's goals and bingo
    board. Render these items together to show a bingo editor.
    """
    rpm = RestaurantProfileManager(app, "Victor Chang")
    goals = rpm.get_goals()
    bingo_board = rpm.get_bingo_board()
    return render_template('index.j2',
                           goals=goals,
                           board_name=bingo_board["name"],
                           board=bingo_board["board"])


@app.route('/save', methods=['POST'])
def save():
    """
    When posting to this route, save a bingo board to the restaurant profile
    using the request body. Redirect to the bingo editor on completion.
    """
    rpm = RestaurantProfileManager(app, "Victor Chang")
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    rpm.set_bingo_board(name, board)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
