from os import getenv
from aiogram import Bot, Dispatcher

BOT_TOKEN = getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main() -> None:
    pass