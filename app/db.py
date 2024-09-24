from pymongo import MongoClient

def get_db():
    """
    Returns the database connection for MongoDB.
    """
    client = MongoClient("mongodb://localhost:27017")
    return client.mydatabase
