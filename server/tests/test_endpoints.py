import uuid
from datetime import UTC, datetime
from unittest import mock

from fastapi.testclient import TestClient


class TestCreateSecret:
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


class TestGetSecret:
    def test__given_id__when_secret_exist_and_not_expired__then_secret_returned(self):
        pass

    def test__given_id__when_does_not_exist__then_404_returned(self):
        pass

    def test__given_id__when_secret_exist_but_expired__then_404_returned(self):
        pass
