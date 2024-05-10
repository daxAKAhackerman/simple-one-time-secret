from db import init_db
from endpoints import router
from fastapi import FastAPI

init_db()

app = FastAPI()

app.include_router(router, prefix="/api/secret", tags=["Secret"])
