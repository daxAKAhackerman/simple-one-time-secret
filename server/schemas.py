from datetime import datetime, timezone
from typing import Annotated

from dateutil.relativedelta import relativedelta
from pydantic import AfterValidator, BaseModel, Field


def is_valid_expiration(value: datetime) -> datetime:
    today = datetime.now(tz=timezone.utc)
    if value > today + relativedelta(months=1):
        raise ValueError("Expiration must be less than a month")
    elif value <= today:
        raise ValueError("Expiration cannot be in the past")
    return value


class CreateSecret(BaseModel):
    expiration: Annotated[datetime, AfterValidator(is_valid_expiration)]
    secret: str = Field(min_length=1, max_length=32000)
