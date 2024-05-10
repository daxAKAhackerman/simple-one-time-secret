import os
import uuid
from typing import Optional

import pymongo
from models import Secret
from pymongo.collection import Collection
from pymongo.database import Database


def init_db() -> None:
    MONGO_SECRET_COL = os.getenv("MONGO_SECRET_COL", "secret")
    secret_collection = get_ots_database()[MONGO_SECRET_COL]
    secret_collection.create_index("expiration", expireAfterSeconds=0)


def get_ots_database() -> Database:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = os.getenv("MONGO_PORT", 27017)
    MONGO_DB = os.getenv("MONGO_DB", "ots")

    mongo_client = pymongo.MongoClient(host=MONGO_HOST, port=int(MONGO_PORT))

    return mongo_client[MONGO_DB]


class SecretStore:
    secret_collection_name: str
    secret_collection: Collection

    def __init__(self) -> None:
        self.secret_collection_name = os.getenv("MONGO_SECRET_COL", "secret")
        self.secret_collection = get_ots_database()[self.secret_collection_name]

    def put_secret(self, secret: Secret) -> Secret:
        self.secret_collection.insert_one(secret.to_mongo_item())
        return secret

    def get_and_delete_secret_by_id(self, id: uuid.UUID) -> Optional[Secret]:
        mongo_item = self.secret_collection.find_one({"_id": str(id)})

        if mongo_item:
            secret = Secret.from_mongo_item(**mongo_item)
            self.secret_collection.delete_one(secret.mongo_id)
            return secret
