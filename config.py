# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from os import getenv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")  # put your bot token here
# BOT_SESSION = AiohttpSession(proxy='http://proxy.server:3128')

ADMIN_PING_TIMEOUT = 10  # 10 seconds

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()