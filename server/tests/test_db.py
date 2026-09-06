import uuid
from collections.abc import Iterator
from typing import cast
from unittest import mock

import pytest
from db import OtsDatabase, SecretStore, init_db


class TestInitDb:
    def test__then_index_created(self, ots_database: dict[str, mock.MagicMock]):
        secret_collection = ots_database["secret"]

        init_db()

        secret_collection.create_index.assert_called_once_with("expiration", expireAfterSeconds=0)


class TestOtsDatabase:
    @pytest.fixture(autouse=True)
    def mongo_client_mock(self) -> Iterator[mock.MagicMock]:
        with mock.patch("db.pymongo.MongoClient") as mocker:
            mocker.return_value = {"ots": "hello"}
            yield mocker

    @pytest.mark.no_ots_database_mocker
    def test____init__then_attributes_set(self, mongo_client_mock: mock.MagicMock):
        ots_database = OtsDatabase()

        mongo_client_mock.assert_called_once_with(host="localhost", port=27017)
        assert ots_database.database == "hello"

    @pytest.mark.no_ots_database_mocker
    def test____new____when_instanciated_twice__then_same_instance(self, mongo_client_mock: mock.MagicMock):
        # Reset the singleton
        OtsDatabase.instance = None

        ots_database_1 = OtsDatabase()
        ots_database_2 = OtsDatabase()

        assert ots_database_1 is ots_database_2
        mongo_client_mock.assert_called_once()


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
        secret_collection.find_one_and_delete.return_value = {"some": "mongo_item"}
        secret = from_mongo_item_mocker.return_value

        ret = secret_store.get_and_delete_secret_by_id(uuid.UUID("11111111-1111-4111-a111-111111111111"))

        secret_collection.find_one_and_delete.assert_called_once_with({"_id": "11111111-1111-4111-a111-111111111111"})
        from_mongo_item_mocker.assert_called_once_with(some="mongo_item")
        assert ret == secret

    def test__get_and_delete_secret_by_id__given_id__when_not_exist__then_none_returned(self):
        secret_store = SecretStore()
        secret_collection = cast(mock.MagicMock, secret_store.secret_collection)
        secret_collection.find_one_and_delete.return_value = None

        secret = secret_store.get_and_delete_secret_by_id(uuid.UUID("11111111-1111-4111-a111-111111111111"))

        assert secret is None
