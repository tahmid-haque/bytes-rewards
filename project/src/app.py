"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

import os
from flask import Flask, render_template, request, redirect, flash
from restaurant_profile_manager import RestaurantProfileManager

app = Flask(__name__)  # Initialize a flask app using current file
app.secret_key = b'averysecretkey'

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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        pass # Register user and do necessary redirect here
    else:
        #flash("An error has occurred!") # Use this to show error messages
        return render_template('create_account.j2')


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
