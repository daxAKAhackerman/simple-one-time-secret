import uuid
from datetime import datetime

import pydantic


class CreateSecretRequestBody(pydantic.BaseModel):

    _id: pydantic.UUID4 = pydantic.PrivateAttr(default_factory=uuid.uuid4)
    expiration: datetime
    secret: str

    def get_mongo_item(self):
        return {"_id": str(self._id), "expiration": self.expiration, "secret": self.secret}
