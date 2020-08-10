"""
This file houses the customer favourite interface.
It is used to interact with the customer profile database for favourites.
"""
from bson.objectid import ObjectId
from modules.database import QueryFailureException


def get_favourite(cpm):
    """
    Gets the list of user's favourite restaurant Ids
	"""
    try:
        customer = cpm.db.query("customers", {"username": cpm.id})[0]
        if "favourite" in customer:
            return customer["favourite"]
        else:
            return []
    except QueryFailureException:
        print("Something's wrong with the query.")
    except IndexError:
        print("Could not find the customer")


def update_favourite(cpm, obj_id):
    """
	Updates the list of user's favourite restaurant Ids
	"""
    try:
        customer = cpm.db.query("customers", {"username": cpm.id})[0]
        if "favourite" not in customer:
            cpm.db.update("customers", {"username": cpm.id},
                          {"$push": {
                              "favourite": ObjectId(obj_id)
                          }})
        else:
            if ObjectId(obj_id) in customer["favourite"]:
                cpm.db.update('customers', {"username": cpm.id},
                              {"$pull": {
                                  "favourite": ObjectId(obj_id)
                              }})
            else:
                cpm.db.update('customers', {"username": cpm.id},
                              {"$push": {
                                  "favourite": ObjectId(obj_id)
                              }})
        return get_favourite(cpm)
    except QueryFailureException:
        print("Something's wrong with the query.")
    except IndexError:
        print("Could not find the customer")


def get_favourite_doc(profiles, favourite):
    """
	Gets a dictionary of the user's favourite restaurant profiles
	"""
    list_fav = {}
    for fav in favourite:
        if fav in profiles:
            list_fav[ObjectId(fav)] = profiles[ObjectId(fav)]
    return list_fav
