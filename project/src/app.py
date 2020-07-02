"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

import os
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from restaurant_profile_manager import RestaurantProfileManager

app = Flask(__name__)  # Initialize a flask app using current file
app.secret_key = b'averysecretkey'

@app.route('/')
def index():
    """
    When retrieving this route, get a restaurant profile's goals and bingo
    board. Render these items together to show a bingo editor.
    """
    '''
    TODO: Changing Victor's profile created a bug.
    rpm = RestaurantProfileManager(app, "Victor Chang", "VChang", "Nothashed1")
    goals = rpm.get_goals()
    bingo_board = rpm.get_bingo_board() #<- There's an issue here. See line 73 in restaurant_profile_manager.py
    return render_template('index.j2',
                           goals=goals,
                           board_name=bingo_board["name"],
                           board=bingo_board["board"])
    '''
    return redirect("/signup") # for now redirect to signup


@app.route('/save', methods=['POST'])
def save():
    """
    When posting to this route, save a bingo board to the restaurant profile
    using the request body. Redirect to the bingo editor on completion.
    """
    rpm = RestaurantProfileManager(app, "Victor Chang", "VChang", "Nothashed1")
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    rpm.set_bingo_board(name, board)
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    When posting to this page, verify the credentials provided. If valid, redirect to homepage.
    Otherwise prompt user.
    TODO:
    """
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    When posting to this page, verify if user already exists. If not, redirect to login.
    """
    if request.method == 'POST':
        fullname = request.form["fullName"]
        username = request.form["username"]
        password = request.form["password"]
        possible_user = RestaurantProfileManager(app, fullname, username, password)
        if possible_user.check_user_exists(username): # A user already exists with this username.
            flash("This username is taken. Please choose a new one.")
            return render_template('create_account.j2') # Let user try again
        else:
        	possible_user.set_new_profile(fullname, username, password) # If they're successful, insert into database
        	return redirect("/login")
    else:
        return render_template('create_account.j2')


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
