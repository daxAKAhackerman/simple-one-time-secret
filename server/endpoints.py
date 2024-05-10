import uuid
from datetime import datetime

from db import SecretStore
from fastapi import APIRouter, HTTPException, status
from models import Secret
from schemas import CreateSecret

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_secret(body: CreateSecret):
    secret_store = SecretStore()
    secret = Secret.from_create_request(**body.model_dump())

    secret_store.put_secret(secret)

    return {"id": secret.id}


@router.get("/{id}")
def get_secret(id: uuid.UUID):
    secret_store = SecretStore()
    secret = secret_store.get_and_delete_secret_by_id(id)

    if not secret or secret.expiration <= datetime.now():
        raise HTTPException(404)

    return {"secret": secret.secret}
