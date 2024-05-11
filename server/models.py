from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime

import pytz


@dataclass
class Secret:
    expiration: datetime
    secret: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @classmethod
    def from_create_request(cls, expiration: datetime, secret: str) -> Secret:
        expiration = expiration.replace(tzinfo=pytz.UTC)
        return Secret(expiration=expiration, secret=secret)

    def to_mongo_item(self) -> dict[str, str | datetime]:
        return {"_id": str(self.id), "expiration": self.expiration, "secret": self.secret}

    @classmethod
    def from_mongo_item(cls, _id: str, expiration: datetime, secret: str) -> Secret:
        expiration = expiration.replace(tzinfo=pytz.UTC)
        return Secret(id=uuid.UUID(_id), expiration=expiration, secret=secret)

    @property
    def mongo_id(self) -> dict[str, str]:
        return {"_id": str(self.id)}
