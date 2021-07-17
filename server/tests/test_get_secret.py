from datetime import datetime
from uuid import UUID

from fastapi import Response

from server.endpoints import get_secret


def test__get_secret__valid_data__secret_returned(dummy_mongo_col):

    response = Response()

    ret = get_secret(UUID("11111111-1111-4111-a111-111111111111"), response)

    assert ret["_id"] == "11111111-1111-4111-a111-111111111111"
    assert isinstance(ret["expiration"], datetime)
    assert ret["secret"] == "some_encrypted_secret"


def test__get_secret__expired_secret__404(dummy_mongo_col):

    response = Response()

    ret: Response = get_secret(UUID("22222222-2222-4222-a222-222222222222"), response)

    assert ret == {"message": "Not Found"}


def test__get_secret__non_existent_secret__404(dummy_mongo_col):

    response = Response()

    ret: Response = get_secret(UUID("33333333-3333-4333-a333-333333333333"), response)

    assert ret == {"message": "Not Found"}
