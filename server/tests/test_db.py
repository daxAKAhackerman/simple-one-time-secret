import uuid
from typing import cast
from unittest import mock

import pytest
from db import SecretStore, get_ots_database, init_db


class TestInitDb:
    def test__then_index_created(self, ots_database: dict[str, mock.MagicMock]):
        secret_collection = ots_database["secret"]

        init_db()

        secret_collection.create_index.assert_called_once_with("expiration", expireAfterSeconds=0)


class TestGetOtsDatabase:
    @pytest.mark.no_ots_database_mocker
    @mock.patch("db.pymongo.MongoClient")
    def test__then_ots_database_returned(self, MongoClientMocker: mock.MagicMock):
        MongoClientMocker.return_value = {"ots": "hello"}

        ots_database = get_ots_database()

        MongoClientMocker.assert_called_once_with(host="localhost", port=27017)
        assert ots_database == "hello"


class TestSecretStore:
    def test____init____then_attributes_correctly_set(self, ots_database: dict[str, mock.MagicMock]):
        secret_collection = ots_database["secret"]
        secret_store = SecretStore()

        assert secret_store.secret_collection_name == "secret"
        assert secret_store.secret_collection == secret_collection

    def test__put_secret__given_secret__then_secret_put(self):
        secret_store = SecretStore()
        secret = mock.MagicMock()
        secret_collection = cast(mock.MagicMock, secret_store.secret_collection)

        ret = secret_store.put_secret(secret)

        secret_collection.insert_one.assert_called_once_with(secret.to_mongo_item.return_value)
        assert ret == secret

    @mock.patch("models.Secret.from_mongo_item")
    def test__get_and_delete_secret_by_id__given_id__when_exist__then_secret_deleted_and_returned(self, from_mongo_item_mocker: mock.MagicMock):
        secret_store = SecretStore()
        secret_collection = cast(mock.MagicMock, secret_store.secret_collection)
        secret_collection.find_one.return_value = {"some": "mongo_item"}
        secret = from_mongo_item_mocker.return_value

        ret = secret_store.get_and_delete_secret_by_id(uuid.UUID("11111111-1111-4111-a111-111111111111"))

        secret_collection.find_one.assert_called_once_with({"_id": "11111111-1111-4111-a111-111111111111"})
        from_mongo_item_mocker.assert_called_once_with(some="mongo_item")
        secret_collection.delete_one.assert_called_once_with(secret.mongo_id)
        assert ret == secret

    def test__get_and_delete_secret_by_id__given_id__when_not_exist__then_none_returned(self):
        secret_store = SecretStore()
        secret_collection = cast(mock.MagicMock, secret_store.secret_collection)
        secret_collection.find_one.return_value = None

        secret = secret_store.get_and_delete_secret_by_id(uuid.UUID("11111111-1111-4111-a111-111111111111"))

        assert secret is None
