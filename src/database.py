"""Module providing Database API."""
from asyncio import sleep
import pymongo
def initialize_db(host, port):
    """Initialize Database."""
    try:
        mongo = pymongo.MongoClient(host+':'+str(port)+'/', connectTimeoutMS=5000)
        print(mongo)
        users = mongo["users"]
        dblist = mongo.list_database_names()
        for db in dblist:
            print(db)
    except Exception as e:
        print(e)
    # if not "users" in dblist:
    #     users = mongo["users"]
    # if not "last_news" in dblist:
    #     last_news = mongo["last_news"]
    return mongo
