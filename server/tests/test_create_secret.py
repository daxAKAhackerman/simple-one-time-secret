from uuid import UUID

from server.endpoints import create_secret
from server.models import CreateSecretRequestBody


def test__create_secret__valid_data__uuid_returned():
    fake_request_body = CreateSecretRequestBody(secret="some_encrypted_secret", expiration=754462800)

    ret = create_secret(fake_request_body)

    assert isinstance(ret["id"], UUID)
