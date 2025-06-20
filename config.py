# from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.state import StatesGroup, State

from os import getenv
from dotenv import load_dotenv


class BotStates(StatesGroup):
    # BASIC_STATE = State()
    CREATE_NEW_THREAD = State()
    ACCEPT_THREAD = State()
    DECLINE_THREAD = State()
    

load_dotenv()

REDIS_URL = getenv("REDIS_URL")
BOT_TOKEN = getenv("BOT_TOKEN")  # put your bot token here
# BOT_SESSION = AiohttpSession(proxy='http://proxy.server:3128')

redis_storage = RedisStorage.from_url(REDIS_URL)

# TODO maybe transfer bot into main function
bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=redis_storage)

ADMIN_PING_TIMEOUT = 10  # 10 seconds
TARGET_CHAT_ID = -4977208701

# TODO transfer text into JSON
KB_BUTTONS = {
    "action_management": {
        "action_cancel": "Отменить действие"
    },
    "thread_management": {
        "thread_1": "Взять диалог",
        "thread_0": "Отказаться",
    },
    "suggestion_management": {
        "suggestion_1": "За предложение",
        "suggestion_0": "Против"
    }
}
