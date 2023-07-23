import logging

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from src.api.v1.file import router as file_router
from src.api.v1.user import router as user_router
from src.core.deps.user import login_required
from src.db.session import get_session
from src.services.redis import redis_client

router = APIRouter(prefix='/v1')

router.include_router(user_router)
router.include_router(file_router, dependencies=[Depends(login_required)])


@router.get('/ping')
async def ping(db: AsyncSession = Depends(get_session)) -> dict:
    logging.info('Ping database')
    db_version = (await db.execute(text("select version()"))).scalar_one_or_none()
    redis_version = redis_client.execute_command('INFO')['redis_version']
    return {
        'db': db_version,
        'redis': redis_version,
    }
