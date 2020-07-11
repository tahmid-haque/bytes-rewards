"""
This is the main component of our customer project. It is be used to connect
the whole app together and provide a way to start a server.
"""

import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from customer_profile_manager import CustomerProfileManager

app = Flask(__name__)  # Initialize a flask app using current file
app.secret_key = b'averysecretkey'
login_manager = LoginManager()
login_manager.init_app(app)  # Initialize login manager for flask app
login_manager.login_view = 'login'  # Redirect to login, as login is required
login_manager.session_protection = "strong"


# Strengthen session cookie protection


@login_manager.user_loader
def load_user(username):
    """
	Load user from database.
	"""
    possible_user = CustomerProfileManager(app, username)
    possible_user.get_user()
    return possible_user


@app.route('/')
def index():
    """
    Redirects user to customer login.
    """
    return redirect("/customer_login")


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    """
    When posting to this page, verify the credentials provided. If valid,
    redirect to homepage. Otherwise prompt user and require them to try again.
    """
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        possible_user = CustomerProfileManager(app, username)
        if possible_user.check_user_exists(username):
            possible_user.get_user(
            )  # Update the possible user with credentials
            if (possible_user and possible_user.check_password(password)):
                login_user(possible_user
                           )  # If username and password are correct, login
                name = possible_user.fullname
                return redirect(
                    url_for('.view_profiles', username=username, name=name))
        flash("Incorrect username or password. Please try again.")
        return render_template('customer_login.j2')
    return render_template('customer_login.j2')


@app.route("/customer_logout")
@login_required
def customer_logout():
    """
    Logs out current user.
    """
    logout_user()
    return redirect('/customer_login')


@app.route('/customer_signup', methods=['GET', 'POST'])
def customer_signup():
    """
    When posting to this page, verify if user already exists. If not, redirect
    to login.
    """
    if request.method == 'POST':
        fullname = request.form["fullName"]
        username = request.form["username"]
        password = request.form["password"]
        possible_user = CustomerProfileManager(app, username)
        if possible_user.check_user_exists(
                username):  # A user already exists with this username.
            flash("This username is taken. Please choose a new one.")
            return render_template(
                'customer_create_account.j2')  # Let user try again
        # If they're successful, insert into database
        possible_user.set_new_profile(fullname, password)
        return redirect("/customer_login")
    return render_template('customer_create_account.j2')


@app.route('/view_profiles', methods=['GET', 'POST'])
@login_required
def view_profiles():
    """
    Allows users to view restaurant profiles that are ready for viewing.
    """
    username = login_manager.user_loader
    name = request.args['name']
    user = CustomerProfileManager(app, username)
    restaurant_users = user.get_restaurant_users()

    return render_template('view_profiles.j2',
                           users=restaurant_users,
                           name=name)


@app.route('/view_board/<string:id>', methods=['GET', 'POST'])
@login_required
def view_board(id):
    """
    Allows users to view restaurant board that they have selected.
    """
    username = login_manager.user_loader
    user = CustomerProfileManager(app, username)
    goals = []
    name = ""
    rewards = []
    restaurant_users = user.get_restaurant_users()
    for restaurant_user in restaurant_users:
        if str(restaurant_user["_id"]) == id:
            name = restaurant_user["bingo_board"]["name"]
            goal_ids = restaurant_user["bingo_board"]["board"]
            for id in goal_ids:
                for goal in user.get_goals():
                    if goal["_id"] == id:
                        goals.append(goal["goal"])
            rewards = restaurant_user["bingo_board"]["board_reward"]
    return render_template('view_game_board.j2', goals=goals, name=name, rewards=rewards)


if __name__ == "__main__":
    app.run(host="localhost", port=os.environ.get('PORT', 8000), debug=True)
