from datetime import datetime

from pydantic import BaseModel, Field


class CreateSecret(BaseModel):
    expiration: datetime
    secret: str = Field(min_length=1)
