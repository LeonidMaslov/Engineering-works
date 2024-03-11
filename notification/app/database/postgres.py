from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.settings import settings

postgres_engine: AsyncEngine = create_async_engine(settings.postgres_db_url)
async_session = async_sessionmaker(postgres_engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    """
    Получение асинхронной сессии для работы с базой данных
    :return: Асинхронная сессия
    """
    async with async_session() as session:
        yield session
