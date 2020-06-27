"""
This file houses all databases-related components. It includes support for all
CRUD operations and provided custom error handling.
"""

import os
from flask_pymongo import PyMongo  # Import Flask-PyMongo utilities

# Exceptions
class QueryFailureException(Exception):
    pass

class Database:
    """
    This class holds all database communication components. It is responsible
    for maintaining a single database instance and providing a communication
    pathway between our app and the remote database.
    """
    instance = None  # Holds a single occurence of the database

    # Indicates mongo server location and corresponding database, "bytes"
    mongoURI = "mongodb+srv://admin:alwW8GtvfSoyHF4e@cluster0-wjxhu.azure.mongodb.net/bytes?retryWrites=true&w=majority"

    @staticmethod
    def get_instance(app):
        """
        Return the database instance if it has been instantiated.
        Otherwise, instantiate an instance and integrate with given Flask app.
        """
        if Database.instance is None:
            Database(app)
        return Database.instance
    @staticmethod
    def replaceObjectID(document):
        """
        Replace all _id values in a JSON-style dictionary document with 
        the MongoDB ObjectID type value. This is a requirement when using
        MongoDB's unique IDs.
        """
        for key in document:
            if isinstance(document[key], dict):
                Database.replaceObjectID(document[key]) # Recursively update nested documents
            elif key == "_id" and not isinstance(key, ObjectId): # Update entry matching {_id: "sdfr23hfk23f23"} to {_id: ObjectID("sdfr23hfk23f23")}
                document[key] = ObjectId(document[key])

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
    
    def query(self, collection, query = {}):
        """
        Locate a list of documents matching a query, from a given collection 
        in the db. By default, the query matches all documents in the collection.
        Throws QueryFailureException on failure. 
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        try:
            return list(self.db[collection].find(query))    # Find using Mongo and convert to list
        except TypeError:   # Ensure successful find
            raise QueryFailureException("TypeError was found!")

    def queryGoal(self, collection, query):
        """
        Locate a document matching a query from a given collection 
        in the db and locate the 'goals' field. The query corresponds to a unique user.
        Throws QueryFailureException on failure. 
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        try:
            return (self.db[collection].find_one(query))['goals']  # Find user goals using Mongo 
        except TypeError:   # Ensure successful find
            raise QueryFailureException("TypeError was found!")
    
    def deleteGoal(self, collection, query, id):
        """
        Locate the document matching a query from a given collection
        in the db. Locate the goal from the id and remove it from the list.
        Throws QueryFailureException on failure. 
        """
        Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        try:
            return (self.db[collection].update(query, { "$pull": {"goals": id}})) #Removes identified goal from list
        except TypeError:   # Ensure successful find
            raise QueryFailureException("TypeError was found!")
