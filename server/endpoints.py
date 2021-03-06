from datetime import datetime

import pydantic
from db import get_mongo_col
from fastapi import APIRouter, Response, status
from models import CreateSecretRequestBody

router = APIRouter()

secret_col = get_mongo_col()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_secret(request_body: CreateSecretRequestBody):
    secret_col.insert_one(request_body.get_mongo_item())

    return {"id": request_body._id}


@router.get("/{id}")
def get_secret(id: pydantic.UUID4, response: Response):
    secret = secret_col.find_one({"_id": str(id)})

    secret_col.delete_one({"_id": str(id)})

    if not secret or secret["expiration"] <= datetime.utcnow():
        response.status_code = 404
        return {"message": "Not Found"}

    else:
        return secret
