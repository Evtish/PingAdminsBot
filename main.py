import logging
from os import getenv
from asyncio import run
from aiogram import Bot, Dispatcher
from handlers import handler_router

BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

dp.include_router(handler_router)


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
