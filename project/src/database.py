"""
This file houses all databases-related components. It includes support for all
CRUD operations and provided custom error handling.
"""

import os, re
from flask_pymongo import PyMongo, ObjectId # Import Flask-PyMongo utilities

# Exceptions
class QueryFailureException(Exception):
    pass

class UpdateFailureException(Exception):
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
        if isinstance(document, dict):
            return {key: Database.replaceObjectID(val) for key, val in document.items()}
        elif isinstance(document, list):
            return [Database.replaceObjectID(val) for val in document]
        elif isinstance(document, str) and ObjectId.is_valid(document): # Update entry matching {_id: "sdfr23hfk23f23"} to {_id: ObjectID("sdfr23hfk23f23")}
            return ObjectId(document)
        return document

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
        try:
            query = Database.replaceObjectID(query) # Update all _id keys for use with Mongo
            return list(self.db[collection].find(query))    # Find using Mongo and convert to list
        except TypeError as e:   # Ensure successful find
            print(e)
            raise QueryFailureException("TypeError was found!")
    
    def update(self, collection, query, document):
        """
        Update the first document from a collection in the db who matches a given query. 
        Throws UpdateFailureException on failure.
        """
        query = Database.replaceObjectID(query) # Update all _id keys for use with Mongo
        res = self.db[collection].update_one(query, document) # Update using Mongo
        if not res.acknowledged:    # Ensure successful update
            raise UpdateFailureException("Failed to update!")

    # def queryGoal(self, collection, query):
    #     """
    #     Locate a document matching a query from a given collection 
    #     in the db and locate the 'goals' field. The query corresponds to a unique user.
    #     Throws QueryFailureException on failure. 
    #     """
    #     try:
    #         return (self.db[collection].find_one(query))['goals']  # Find user goals using Mongo 
    #     except TypeError:   # Ensure successful find
    #         raise QueryFailureException("TypeError was found!")
    
    # def deleteGoal(self, collection, query, value):
    #     """
    #     Locate the document matching a query from a given collection
    #     in the db. Locate the goal from the id and remove it from the list.
    #     Throws QueryFailureException on failure. 
    #     """
    #     try:
    #         return (self.db[collection].update(query, { "$pull": {"goals": value}})) #Removes identified goal from list
    #     except TypeError:   # Ensure successful find
    #         raise QueryFailureException("TypeError was found!")

    # def addGoal(self, collection, query, value, position):
    #     """
    #     Locate the document matching a query from a given collection
    #     in the db. Locate the goal from the id and add it from the list.
    #     Throws QueryFailureException on failure. 
    #     """
    #     if value == "0": #check that a value has been chosen
    #         return None
    #     goal = re.search('\'goal\': \'(.*?)\'', value).group(1) #search for goal
    #     try:
    #         return (self.db[collection].update(query, { "$push": {"goals": { "$each": [goal], "$position": position}}})) #Adds identified goal from list
    #     except TypeError:   # Ensure successful find
    #         raise QueryFailureException("TypeError was found!")
