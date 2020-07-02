"""
This file houses all databases-related components. It includes support for all
CRUD operations and provided custom error handling.
"""

from flask_pymongo import PyMongo, ObjectId  # Import Flask-PyMongo utilities


class QueryFailureException(Exception):
    """
    Exception class used to indicate failure resolving a database query.
    """


class UpdateFailureException(Exception):
    """
    Exception class used to indicate failure updating a database.
    """


class InsertFailureException(Exception):
    """
    Exception class used to indicate failure inserting into a database.
    """


class Database:
    """
    This class holds all database communication components. It is responsible
    for maintaining a single database instance and providing a communication
    pathway between our app and the remote database.
    """
    instance = None  # Holds a single occurence of the database

    # Indicates mongo server location and corresponding database, "bytes"
    mongoURI = "mongodb+srv://admin:alwW8GtvfSoyHF4e@cluster0-wjxhu." +\
               "azure.mongodb.net/bytes?retryWrites=true&w=majority"

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
    def replace_object_id(document):
        """
        Replace all _id values in a JSON-style dictionary document with
        the MongoDB ObjectID type value. This is a requirement when using
        MongoDB's unique IDs. (i.e # Update entry matching
        {_id: "sdfr23hfk23f23"} to {_id: ObjectID("sdfr23hfk23f23")})
        """
        if isinstance(document, dict):
            return {
                key: Database.replace_object_id(val)
                for key, val in document.items()
            }
        if isinstance(document, list):
            return [Database.replace_object_id(val) for val in document]
        if isinstance(document, str) and ObjectId.is_valid(document):
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

    def query(self, collection, query={}):
        """
        Locate a list of documents matching a query, from a given collection
        in the db. By default, the query matches all documents in the
        collection. Throws QueryFailureException on failure.
        """
        try:
            query = Database.replace_object_id(
                query)  # Update all _id keys for use with Mongo
            return list(self.db[collection].find(query))
        except TypeError as error:
            print(error)
            raise QueryFailureException("TypeError was found!")

    def update(self, collection, query, document):
        """
        Update the first document from a collection in the db who matches a
        given query. Throws UpdateFailureException on failure.
        """
        query = Database.replace_object_id(
            query)  # Update all _id keys for use with Mongo
        res = self.db[collection].update_one(query, document)
        if not res.acknowledged:
            raise UpdateFailureException("Failed to update!")

    def insert(self, collection, document):
        """
        Insert a single document into the given collection within the db.
        Throws InsertFailureException on failure.
        """
        res = self.db[collection].insert_one(document)  # Insert using Mongo
        if not res.acknowledged:    # Ensure successful insert
            raise InsertFailureException("Failed to insert!")