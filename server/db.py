import os
import uuid
from typing import Self

import pymongo
from models import Secret
from pymongo.collection import Collection
from pymongo.database import Database


def init_db() -> None:
    MONGO_SECRET_COL = os.getenv("MONGO_SECRET_COL", "secret")
    secret_collection = OtsDatabase().database[MONGO_SECRET_COL]
    secret_collection.create_index("expiration", expireAfterSeconds=0)


class OtsDatabase:
    database: Database
    instance: Self | None = None

    def __init__(self) -> None:
        mongo_host = os.getenv("MONGO_HOST", "localhost")
        mongo_port = os.getenv("MONGO_PORT", "27017")
        mongo_db = os.getenv("MONGO_DB", "ots")

        mongo_client = pymongo.MongoClient(host=mongo_host, port=int(mongo_port))
        self.database = mongo_client[mongo_db]

    def __new__(cls) -> Self:
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance


class SecretStore:
    secret_collection_name: str
    secret_collection: Collection

    def __init__(self) -> None:
        self.secret_collection_name = os.getenv("MONGO_SECRET_COL", "secret")
        self.secret_collection = OtsDatabase().database[self.secret_collection_name]

    def put_secret(self, secret: Secret) -> Secret:
        self.secret_collection.insert_one(secret.to_mongo_item())
        return secret

    def get_and_delete_secret_by_id(self, id: uuid.UUID) -> Secret | None:
        mongo_item = self.secret_collection.find_one_and_delete({"_id": str(id)})

        if mongo_item:
            secret = Secret.from_mongo_item(**mongo_item)
            return secret
