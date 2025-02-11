import logging

from asyncio import run

from config import bot, dp
from handlers import router

dp.include_router(router)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
