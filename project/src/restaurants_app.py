"""
This is the main component of our restaurant owner interface. It is used to connect the whole
owner app together and provide a way to start a server.
"""

import os
from flask import Flask, redirect
from modules.restaurant_profile_manager import RestaurantProfileManager
from routes.authentication import get_auth_routes, add_auth
from routes.restaurants.profile import bp as profile_routes
from routes.restaurants.board import bp as board_routes
from routes.restaurants.customize import bp as customize_routes
from routes.restaurants.verification import bp as verification_routes

# Initialize a flask app using current file
app = Flask(__name__,
            template_folder="templates/restaurants",
            static_folder="static/restaurants")
add_auth(app, RestaurantProfileManager)
app.register_blueprint(get_auth_routes(RestaurantProfileManager))
app.register_blueprint(profile_routes, url_prefix="/profile")
app.register_blueprint(board_routes, url_prefix="/board")
app.register_blueprint(verification_routes, url_prefix="/verification")
app.register_blueprint(customize_routes, url_prefix="/customize")


@app.route('/')
def index():
    """
    Redirect to the view profile page.
    """
    return redirect("/profile")


if __name__ == "__main__":
    app.run(debug=True)
