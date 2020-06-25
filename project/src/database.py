"""
This file houses all databases-related components. It includes support for all
CRUD operations and provided custom error handling.
"""

import os
from flask_pymongo import PyMongo  # Import Flask-PyMongo utilities


class Database:
    """
    This class holds all database communication components. It is responsible
    for maintaining a single database instance and providing a communication
    pathway between our app and the remote database.
    """
    instance = None  # Holds a single occurence of the database

    # Indicates mongo server location and corresponding database, "bytes"
    mongoURI = os.environ['BYTES_MONGO_URI'] or "mongodb://localhost:27017/bytes"

    @staticmethod
    def get_instance(app):
        """
        Return the database instance if it has been instantiated.
        Otherwise, instantiate an instance and integrate with given Flask app.
        """
        if Database.instance is None:
            Database(app)
        return Database.instance

    def __init__(self, app):
        """
        Initialize the database object and integrate with the Flask app.
        """
        if Database.instance is not None:
            raise Exception("This class follows singleton patterns! Use \
                getInstance.")

        # Integrate Mongo w/ Flask and save database to object
        app.config["MONGO_URI"] = Database.mongoURI
        self.db = PyMongo(app).db
        Database.instance = self

    # TODO: Add insert, delete methods for deliverable 3
