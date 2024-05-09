from db import create_index
from endpoints import router
from fastapi import FastAPI

create_index()

app = FastAPI()

app.include_router(router, prefix="/api/secret", tags=["Secret"])
