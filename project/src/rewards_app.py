"""
This is the main component of our rewards interface. It is used to connect
the whole rewards app together and provide a way to start a server.
"""

import os
from flask import Flask, redirect
from flask_qrcode import QRcode
from modules.customer.customer_profile_manager import CustomerProfileManager
from routes.authentication import get_auth_routes, add_auth
from routes.rewards.profile import bp as profile_routes
from routes.rewards.restaurants import bp as restaurant_routes

app = Flask(
    __name__,
    template_folder="templates/rewards",
    static_folder="static/rewards")  # Initialize a flask app using current file
add_auth(app, CustomerProfileManager)
QRcode(app)
app.register_blueprint(get_auth_routes(CustomerProfileManager))
app.register_blueprint(profile_routes, url_prefix="/personal")
app.register_blueprint(restaurant_routes, url_prefix="/restaurants")


@app.route('/')
def index():
    """
    Redirect to the view profiles page.
    """
    return redirect("/restaurants")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 7000), debug=True)
