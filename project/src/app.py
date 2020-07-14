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
    # This route will need to be updated with the restaurant summary page
    # Move goals editor to different route

    profile = current_user.get_profile()
    if profile == {}:
        flash("Please create a restaurant profile to continue.")
        return redirect("/profile/edit")

    goals = current_user.get_goals(
    )  # current_user is loaded from load_user so get goals
    bingo_board = current_user.get_bingo_board()
    rewards = current_user.get_rewards()
    return render_template(
        'index.j2',
        goals=goals,
        board_name=bingo_board["name"],
        rewards=rewards,
        board=bingo_board["board"],
        board_reward=bingo_board["board_reward"])


@app.route('/save', methods=['POST'])
@login_required
def save():
    """
    When posting to this route, save a bingo board to the restaurant profile
    using the request body. Redirect to the bingo editor on completion.
    """
    name = request.form["board_name"]
    board = request.form.getlist("board[]")
    board_reward = request.form.getlist("board_reward[]")
    current_user.set_bingo_board(name, board, board_reward)
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
        if possible_user.check_user_exists():
            possible_user.get_user(
            )  # Update the possible user with credentials
            if possible_user and possible_user.check_password(password):
                login_user(possible_user
                          )  # If username and password are correct, login
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
        ):  # A user already exists with this username.
            flash("This username is taken. Please choose a new one.")
            return render_template('create_account.j2')  # Let user try again
        # If they're successful, insert into database
        possible_user.set_new_profile(fullname, password)
        login_user(possible_user)
        return redirect("/profile/edit")
    return render_template('create_account.j2')

@app.route('/profile')
@login_required
def view_profile():
    """
    Displays the current user's restaurant profile page.
    """
    rest_info = current_user.get_profile()
    if rest_info != {}: # Only get the rest info if available.
        return render_template('view_profile.j2',
                               restaurant_name=rest_info["name"],
                               address=rest_info["location"]["address"],
                               city=rest_info["location"]["city"],
                               province=rest_info["location"]["province"],
                               postal_code=rest_info["location"]["postal_code"],
                               phone_number=rest_info["phone_number"],
                               category=rest_info["category"],
                               rest_img=rest_info["image"],
                               description=rest_info["description"])

@app.route('/profile/edit')
@login_required
def edit_profile():
    """
    Display the edit restaurant profile page.
    Prerequisite: User is logged in.
    """
    profile = current_user.get_profile()
    return render_template('edit_profile.j2', profile=profile)


@app.route('/profile/save', methods=['POST'])
@login_required
def save_profile():
    """
    Save a restaurant profile using the provided data.
    Prerequisite: User is logged in.
    """
    profile = {key: val for key, val in request.form.items() if '[' not in key}
    profile["location"] = {}
    for key in request.form:  # Add location items to profile
        if '[' in key:
            profile["location"][key[9:-1]] = request.form[key]
    current_user.update_profile(profile)
    return redirect("/")

@app.route('/profile/edit')
@login_required
def edit_profile():
    """
    Display the edit restaurant profile page.
    Prerequisite: User is logged in.
    """
    profile = current_user.get_profile()
    return render_template('edit_profile.j2', profile=profile)


@app.route('/profile/save', methods=['POST'])
@login_required
def save_profile():
    """
    Save a restaurant profile using the provided data.
    Prerequisite: User is logged in.
    """
    profile = {key: val for key, val in request.form.items() if '[' not in key}
    profile["location"] = {}
    for key in request.form:  # Add location items to profile
        if '[' in key:
            profile["location"][key[9:-1]] = request.form[key]
    current_user.update_profile(profile)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
