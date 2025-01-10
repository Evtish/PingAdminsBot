from aiogram.filters import Command
from aiogram.types import Message

from main import dp
from utils import get_admin_usernames, limit_msg_length


@dp.message(Command("ping"))
async def ping_admins(message: Message) -> None:
    pass