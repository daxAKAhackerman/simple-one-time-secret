import uuid
from datetime import UTC, datetime
from unittest import mock

import pytz
from fastapi.testclient import TestClient
from freezegun import freeze_time


class TestCreateSecret:
    @freeze_time("2024-05-14")
    @mock.patch("endpoints.SecretStore")
    @mock.patch("endpoints.Secret.from_create_request")
    def test__given_expiration_and_secret__then_secret_created(
        self, from_create_request_mocker: mock.MagicMock, SecretStoreMocker: mock.MagicMock, test_client: TestClient
    ):
        secret_store = SecretStoreMocker.return_value
        secret = from_create_request_mocker.return_value
        secret.id = uuid.UUID("11111111-1111-4111-a111-111111111111")

        response = test_client.post("api/secret", json={"expiration": 1715745600, "secret": "my-secret"})

        from_create_request_mocker.assert_called_once_with(secret="my-secret", expiration=datetime.fromtimestamp(1715745600, UTC))
        secret_store.put_secret.assert_called_once_with(secret)
        assert response.status_code == 201
        assert response.json() == {"id": "11111111-1111-4111-a111-111111111111"}

    @freeze_time("2024-05-14")
    def test__given_expiration_in_the_past__then_422_returned(self, test_client: TestClient):
        response = test_client.post("api/secret", json={"expiration": 1715472000, "secret": "my-secret"})

        assert response.status_code == 422

    @freeze_time("2024-05-14")
    def test__given_expiration_too_far_in_the_future__then_422_returned(self, test_client: TestClient):
        response = test_client.post("api/secret", json={"expiration": 1718668800, "secret": "my-secret"})

        assert response.status_code == 422

    @freeze_time("2024-05-14")
    def test__given_secret_too_large__then_422_returned(self, test_client: TestClient):
        response = test_client.post("api/secret", json={"expiration": 1715745600, "secret": "x" * 200_001})

        assert response.status_code == 422


class TestGetSecret:
    @freeze_time("2023-03-07")
    @mock.patch("endpoints.SecretStore")
    def test__given_id__when_secret_exist_and_not_expired__then_secret_returned(self, SecretStoreMocker: mock.MagicMock, test_client: TestClient):
        secret_store = SecretStoreMocker.return_value
        secret = mock.MagicMock()
        secret.expiration = datetime(2023, 3, 8, tzinfo=pytz.UTC)
        secret.secret = "my-secret"
        secret_store.get_and_delete_secret_by_id.return_value = secret

        response = test_client.get("api/secret/11111111-1111-4111-a111-111111111111")

        secret_store.get_and_delete_secret_by_id.assert_called_once_with(uuid.UUID("11111111-1111-4111-a111-111111111111"))
        assert response.status_code == 200
        assert response.json() == {"secret": "my-secret"}

    @mock.patch("endpoints.SecretStore")
    def test__given_id__when_does_not_exist__then_404_returned(self, SecretStoreMocker: mock.MagicMock, test_client: TestClient):
        secret_store = SecretStoreMocker.return_value
        secret_store.get_and_delete_secret_by_id.return_value = None

        response = test_client.get("api/secret/11111111-1111-4111-a111-111111111111")

        assert response.status_code == 404

    @freeze_time("2023-03-07")
    @mock.patch("endpoints.SecretStore")
    def test__given_id__when_secret_exist_but_expired__then_404_returned(self, SecretStoreMocker: mock.MagicMock, test_client: TestClient):
        secret_store = SecretStoreMocker.return_value
        secret = mock.MagicMock()
        secret.expiration = datetime(2023, 3, 6, tzinfo=pytz.UTC)
        secret_store.get_and_delete_secret_by_id.return_value = secret

        response = test_client.get("api/secret/11111111-1111-4111-a111-111111111111")

        assert response.status_code == 404
