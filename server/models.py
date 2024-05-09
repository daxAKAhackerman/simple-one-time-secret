from __future__ import annotations

import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from db import get_ots_database
from pymongo.collection import Collection


@dataclass
class Secret:
    expiration: datetime
    secret: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_create_request(cls, expiration: datetime, secret: str) -> Secret:
        return Secret(expiration=expiration, secret=secret)

    def to_mongo_item(self) -> dict[str, str | datetime]:
        return {"_id": str(self.id), "expiration": self.expiration, "secret": self.secret}

    @classmethod
    def from_mongo_item(cls, _id: str, expiration: datetime, secret: str):
        return Secret(id=uuid.UUID(_id), expiration=expiration, secret=secret)

    @property
    def mongo_id(self) -> dict[str, str]:
        return {"_id": str(self.id)}


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
