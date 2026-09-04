from datetime import datetime, timezone
from typing import Annotated

from dateutil.relativedelta import relativedelta
from pydantic import AfterValidator, BaseModel, Field


def is_less_than_one_year_away(value: datetime) -> datetime:
    today = datetime.now(tz=timezone.utc)
    if value > today + relativedelta(months=1):
        raise ValueError("Expiration must be less than a month")
    return value


class CreateSecret(BaseModel):
    expiration: Annotated[datetime, AfterValidator(is_less_than_one_year_away)]
    secret: str = Field(min_length=1, max_length=900000)
