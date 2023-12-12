"""Module providing Database API."""
from asyncio import sleep
import pymongo
def initialize_db(host, port):
    """Initialize Database."""
    try:
        mongo = pymongo.MongoClient(host+':'+str(port)+'/', connectTimeoutMS=5000)
        users = mongo["users"]
    except Exception as e:
        print(e)
    return mongo
