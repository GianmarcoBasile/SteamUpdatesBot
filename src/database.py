"""Module providing Database API."""
import pymongo


def initialize_db(host, port):
    """Initialize Database."""
    try:
        mongo = pymongo.MongoClient(host + ":" + str(port) + "/", connectTimeoutMS=5000)
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print("Error connecting to the database: " + str(e))
        return None
    return mongo
