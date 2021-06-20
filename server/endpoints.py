from datetime import datetime

import pydantic
from fastapi import APIRouter, Response, status

from db import secret_col
from models import CreateSecretRequestBody

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_secret(request_body: CreateSecretRequestBody):

    secret_col.insert_one(request_body.get_mongo_item())

    return {"message": "Secret created", "id": request_body._id}


@router.get("/{id}")
def get_secret(id: pydantic.UUID4):

    secret = secret_col.find_one({"_id": str(id)})

    secret_col.delete_one({"_id": str(id)})

    if not secret or secret["expiration"] <= datetime.utcnow():
        return Response(status_code=404)

    else:
        return secret
