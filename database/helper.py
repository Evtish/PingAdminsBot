from sqlalchemy import select

from typing import Any, Sequence

from .models import Base
from .connection import Session


async def insert_row(model: Base, **columns: Any) -> None:
    async with Session.begin() as session:
        session.add(model(**columns))


async def select_row(model: Base, **columns: Any) -> Sequence[Any]:
    async with Session() as session:
        result = await session.scalars(
            select(model)
            .filter_by(**columns)
        )
        return result.all()


async def delete_row(model: Base, **columns: Any) -> None:
    async with Session.begin() as session:
        row_to_delete = await select_row(model, **columns)
        await session.delete(*row_to_delete)
