from fastapi import FastAPI

from src.core.config import settings
from src.api.v1.base import router as base_router


app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(base_router, prefix='/api')
