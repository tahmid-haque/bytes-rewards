"""
This is the main component of our project. It is be used to connect the whole
app together and provide a way to start a server.
"""

from flask import Flask
from database import Database

app = Flask(__name__)  # Initialize a flask app using current file
db = Database.get_instance(app)  # Get a database instance
