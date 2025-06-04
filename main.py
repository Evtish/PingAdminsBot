import logging

from asyncio import run

from config import bot, dp
from handlers import main_handler_router
from database.connection import create_tables, engine

dp.include_router(main_handler_router)


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    # await create_tables(engine)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
