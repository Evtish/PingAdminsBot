from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)

from .models import Base

engine = create_async_engine(
    'sqlite+aiosqlite:///main.db?check_same_thread=False',
    echo=True
)

Session = async_sessionmaker(engine)


async def create_tables(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)