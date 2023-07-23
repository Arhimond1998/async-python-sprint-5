from src.core.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine


test_engine: AsyncEngine = create_async_engine(
    settings.TEST_SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=True,
    connect_args={"server_settings": {"application_name": settings.PROJECT_NAME}}
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_test_db() -> AsyncSession:
    async with async_session() as session:
        yield session
