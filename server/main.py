from db import get_mongo_col
from endpoints import router
from fastapi import FastAPI

secret_col = get_mongo_col()
secret_col.create_index("expiration", expireAfterSeconds=0)

app = FastAPI()

app.include_router(router, prefix="/api/secret", tags=["Secret"])
