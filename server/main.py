from endpoints import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router, prefix="/api/secret", tags=["Secret"])
