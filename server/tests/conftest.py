import os
from datetime import datetime, timedelta

os.environ["TESTING"] = "1"


class FakeSecretCol:
    def insert_one(item):
        pass

    def delete_one(query):
        pass

    def find_one(query):
        if query["_id"] == "11111111-1111-4111-a111-111111111111":
            return {"_id": "11111111-1111-4111-a111-111111111111", "secret": "some_encrypted_secret", "expiration": datetime.now() + timedelta(days=1)}
        elif query["_id"] == "22222222-2222-4222-a222-222222222222":
            return {"_id": "22222222-2222-4222-a222-222222222222", "secret": "some_encrypted_secret", "expiration": datetime.now() - timedelta(days=1)}
        return
