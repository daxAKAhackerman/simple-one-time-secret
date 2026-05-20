from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, field_validator

MAX_SECRET_LENGTH = 200_000
MAX_EXPIRATION = timedelta(days=30)


class CreateSecret(BaseModel):
    expiration: datetime
    secret: str = Field(min_length=1, max_length=MAX_SECRET_LENGTH)

    @field_validator("expiration")
    @classmethod
    def expiration_within_bounds(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        now = datetime.now(UTC)
        if value <= now:
            raise ValueError("expiration must be in the future")
        if value > now + MAX_EXPIRATION:
            raise ValueError(f"expiration cannot be more than {MAX_EXPIRATION.days} days in the future")
        return value
