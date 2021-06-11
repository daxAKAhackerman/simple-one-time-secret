import uuid
from datetime import datetime

import pydantic


class CreateSecretRequestBody(pydantic.BaseModel):

    _id: pydantic.UUID4 = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    _timestamp: datetime = pydantic.PrivateAttr(default_factory=datetime.now)
    expiration: datetime
    secret: str

    def get_mongo_item(self):

        return {"_id": str(self._id), "timestamp": int(self._timestamp.timestamp()), "expiration": int(self.expiration.timestamp()), "secret": self.secret}
