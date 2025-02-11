# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from os import getenv

BOT_TOKEN = getenv("BOT_TOKEN")  # put your bot token here
# BOT_SESSION = AiohttpSession(proxy='http://proxy.server:3128')

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))

dp = Dispatcher()