import uuid
from datetime import datetime
from typing import cast
from unittest import mock

import pytz
from models import Secret


class TestSecret:
    def test__from_create_request__given_expiration_and_secret__then_secret_returned(self):
        secret = Secret.from_create_request(datetime(2023, 3, 7), "my-secret")

        assert secret.expiration == datetime(2023, 3, 7, tzinfo=pytz.UTC)
        assert secret.secret == "my-secret"
        assert isinstance(secret.id, uuid.UUID)

    def test__to_mongo_item__then_mongo_item_returned(self):
        secret = Secret(datetime(2023, 3, 7), "my-secret")
        mongo_item = secret.to_mongo_item()
        mongo_item_id = mongo_item["_id"]

        assert mongo_item == {
            "_id": mock.ANY,
            "expiration": datetime(2023, 3, 7),
            "secret": "my-secret",
        }

        mongo_item_id = cast(str, mongo_item_id)
        uuid.UUID(mongo_item_id)

    def test__from_mongo_item__given_mongo_item__then_secret_returned(self):
        secret = Secret.from_mongo_item("11111111-1111-4111-a111-111111111111", datetime(2023, 3, 7), "my-secret")

        assert secret.expiration == datetime(2023, 3, 7, tzinfo=pytz.UTC)
        assert secret.secret == "my-secret"
        assert secret.id == uuid.UUID("11111111-1111-4111-a111-111111111111")

    def test__mongo_id__then_mongo_id_returned(self):
        secret = Secret(datetime(2023, 3, 7), "my-secret", uuid.UUID("11111111-1111-4111-a111-111111111111"))

        assert secret.mongo_id == {"_id": "11111111-1111-4111-a111-111111111111"}
