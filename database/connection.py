from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)

from .models import Base

# создание движка (асинхронный SQLite)
engine = create_async_engine(
    'sqlite+aiosqlite:///main.db?check_same_thread=False',
    echo=True
)

# фабрика сессий
Session = async_sessionmaker(engine)


async def create_tables(engine: AsyncEngine) -> None:
    """cоздание таблиц БД"""

    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)