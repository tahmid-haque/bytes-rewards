"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

import os
from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from restaurant_profile_manager import RestaurantProfileManager

app = Flask(__name__)  # Initialize a flask app using current file
app.secret_key = b'averysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)  # Initialize login manager for flask app
login_manager.login_view = 'login'  # Redirect to login, as login is required
login_manager.session_protection = "strong"  # Strengthen session cookie protection


@login_manager.user_loader
def load_user(username):
    """
    Load user from database.
    """
    possible_user = RestaurantProfileManager(app, username)
    possible_user.get_user()
    return possible_user


@app.route('/')
@login_required
def index():
    """
    When retrieving this route, get a restaurant profile's goals and bingo
    board. Render these items together to show a bingo editor.
    """
    goals = current_user.get_goals(
    )  # current_user is loaded from load_user so get goals
    bingo_board = current_user.get_bingo_board()
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
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    current_user.set_bingo_board(name, board)
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    When posting to this page, verify the credentials provided. If valid, redirect to homepage.
    Otherwise prompt user and require them to try again.
    """
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        possible_user = RestaurantProfileManager(app, username)
        if possible_user.check_user_exists(username):
            possible_user.get_user(
            )  # Update the possible user with credentials
            if possible_user and possible_user.check_password(password):
                login_user(possible_user)  # If username and password are correct, login
                return redirect("/")
        flash("Incorrect username or password. Please try again.")
    return render_template('login.j2')


@app.route("/logout")
@login_required
def logout():
    """
    Logs out current user. TODO: Make sure you do this, or you'll always end up on signup
    """
    logout_user()
    return redirect('/login')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    When posting to this page, verify if user already exists.
    If user does not exist and form follows format, redirect to login.
    """
    if request.method == 'POST':
        fullname = request.form["fullName"]
        username = request.form["username"]
        password = request.form["password"]
        possible_user = RestaurantProfileManager(app, username)
        if possible_user.check_user_exists(
                username):  # A user already exists with this username.
            flash("This username is taken. Please choose a new one.")
            return render_template('create_account.j2')  # Let user try again
        # If they're successful, insert into database
        possible_user.set_new_profile(fullname, password)
        return redirect("/login")
    return render_template('create_account.j2')

@app.route('/profile')
def view_profile():
    """
    Displays the current user's restaurant profile page.
    """
    rest_info = current_user.get_profile()
    address =''
    for lc in rest_info["location"]: # Get all elements of location
        address += rest_info["location"][lc] + ' '
    if rest_info != {}: # Only get the rest info if available.
        return render_template('view_profile.j2',
                               restaurant_name=rest_info["name"],
                               address=address[:-1], # Remove trailing whitespace
                               phone_number=rest_info["phone_number"],
                               categories=rest_info["category"],
                               rest_img=rest_info["image"],
                               description=rest_info["description"])
    else: # Otherwise return default
        return render_template('view_profile.j2')

if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
