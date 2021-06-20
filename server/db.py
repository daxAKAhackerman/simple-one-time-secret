import os

import pymongo

MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = os.environ["MONGO_PORT"]
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
MONGO_DB = os.environ["MONGO_DB"]
MONGO_COL = os.environ["MONGO_COL"]

mongo_client = pymongo.MongoClient(host=MONGO_HOST, port=int(MONGO_PORT), username=MONGO_USERNAME, password=MONGO_PASSWORD)

secret_col = mongo_client[MONGO_DB][MONGO_COL]

secret_col.create_index("expiration", expireAfterSeconds=0)
