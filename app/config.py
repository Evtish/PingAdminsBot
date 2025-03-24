# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State

from os import getenv
from dotenv import load_dotenv


class BotStates(StatesGroup):
    BASIC_STATE = State()
    CREATE_NEW_THREAD = State()
    SET_TARGET_CHAT = State()
    

load_dotenv()

BOT_TOKEN = getenv("BOT_TOKEN")  # put your bot token here
# BOT_SESSION = AiohttpSession(proxy='http://proxy.server:3128')

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

ADMIN_PING_TIMEOUT = 10  # 10 seconds
TARGET_CHAT_ID = -1001692257147
