import os
from datetime import datetime

import pytest

os.environ["MONGO_HOST"] = "db"
os.environ["MONGO_PORT"] = "31337"
os.environ["MONGO_USERNAME"] = "user"
os.environ["MONGO_PASSWORD"] = "password"
os.environ["MONGO_DB"] = "ots"
os.environ["MONGO_COL"] = "secret"


@pytest.fixture
def dummy_mongo_col(mocker):
    class FakeSecretCol:
        def insert_one(item):
            pass

        def delete_one(query):
            pass

        def find_one(query):
            if query["_id"] == "11111111-1111-4111-a111-111111111111":
                return {"_id": "11111111-1111-4111-a111-111111111111", "secret": "some_encrypted_secret", "expiration": datetime(9999, 1, 1, 0, 0)}
            elif query["_id"] == "22222222-2222-4222-a222-222222222222":
                return {"_id": "22222222-2222-4222-a222-222222222222", "secret": "some_encrypted_secret", "expiration": datetime(2000, 1, 1, 0, 0)}
            return

    mocker.patch("server.endpoints.get_mongo_col", return_value=FakeSecretCol)
