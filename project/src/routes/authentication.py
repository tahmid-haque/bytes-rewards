"""
This file contains the necessary routes and methods that are required for authentication of
users.
"""

from flask import render_template, request, redirect, flash, Blueprint
from flask_login import LoginManager, current_user, login_user, login_required, logout_user


def add_auth(app, profile_manager):
    """
    Add authentication capabilities to the given app.
    """
    login_manager = LoginManager()
    login_manager.init_app(app)  # Initialize login manager for flask app
    login_manager.login_view = '/login'  # Redirect to login, as login is required
    login_manager.session_protection = "strong"  # Strengthen session cookie protection
    app.secret_key = b'averysecretkey'

    @login_manager.user_loader
    def load_user(username):
        """
        Load user from database.
        """
        possible_user = profile_manager(username)
        possible_user.get_user()
        return possible_user


def get_auth_routes(profile_manager):
    """
    Return a blueprint based upon a given profile manager that contains all authentication routes.
    """
    bp = Blueprint('authentication', __name__)

    @bp.route('/login', methods=['GET', 'POST'])
    def login():
        """
        When posting to this route, verify the credentials provided. If valid, redirect to homepage.
        Otherwise prompt user and require them to try again.
        """
        if current_user.is_authenticated:
            current_user.update_board()
            return redirect("/")

        if request.method == 'POST':
            username = request.form["username"]
            password = request.form["password"]
            possible_user = profile_manager(username)
            if possible_user.check_user_exists():
                possible_user.get_user(
                )  # Update the possible user with credentials
                if possible_user and possible_user.check_password(password):
                    login_user(possible_user
                              )  # If username and password are correct, login
                    current_user.update_board()
                    return redirect("/")
            flash("Incorrect username or password. Please try again.")
        return render_template('login.j2')

    @bp.route("/logout")
    @login_required
    def logout():
        """
        Logs out current user.
        """
        logout_user()
        return redirect('/login')

    @bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        """
        When posting to this page, verify if user already exists.
        If user does not exist and form follows format, redirect to login.
        """
        if request.method == 'POST':
            fullname = request.form["fullName"]
            username = request.form["username"]
            password = request.form["password"]
            possible_user = profile_manager(username)
            if possible_user.check_user_exists(
            ):  # A user already exists with this username.
                flash("This username is taken. Please choose a new one.")
                return render_template(
                    'create_account.j2')  # Let user try again
            # If they're successful, insert into database
            possible_user.set_new_profile(fullname, password)
            login_user(possible_user)
            return redirect("/")
        return render_template('create_account.j2')

    return bp
