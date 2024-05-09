import os

import pymongo
from pymongo.database import Database


def create_index() -> None:
    MONGO_SECRET_COL = os.getenv("MONGO_SECRET_COL", "secret")
    secret_collection = get_ots_database()[MONGO_SECRET_COL]
    secret_collection.create_index("expiration", expireAfterSeconds=0)


def get_ots_database() -> Database:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", 27017)
    MONGO_DB = os.getenv("MONGO_DB", "ots")

    mongo_client = pymongo.MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))

    return mongo_client[MONGO_DB]
