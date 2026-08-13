from fastapi import FastAPI

from app.api.v1 import ALL_ROUTERS
from app.core.config import settings

app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check():
    return {"status": "ok"}


for router in ALL_ROUTERS:
    app.include_router(router, prefix="/api/v1")
