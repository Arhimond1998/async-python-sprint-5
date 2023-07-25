import shutil
from pathlib import Path

import asyncio
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from src.core.config import settings
from test.unit_test.db import get_test_db, test_engine


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for every test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def app_instance() -> FastAPI:
    from src.main import app
    from src.db.db import Base
    from src.models import FileTable, UserTable # noqa
    from src.db.session import get_session

    meta = Base.metadata

    async with test_engine.begin() as conn:
        await conn.run_sync(meta.drop_all)
        await conn.run_sync(meta.create_all)
    settings.UPLOAD_FOLDER = settings.TEST_UPLOAD_FOLDER
    app.dependency_overrides[get_session] = get_test_db
    return app


@pytest.fixture(scope='session')
def base_url() -> str:
    return 'http://test'


@pytest.fixture(scope='session')
async def client(app_instance: FastAPI, base_url: str) -> AsyncClient:
    async with AsyncClient(app=app_instance, base_url=base_url) as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
def directory_cleanup():
    p = Path() / settings.UPLOAD_FOLDER
    p.mkdir(parents=True, exist_ok=True)
    yield
    shutil.rmtree(p)
