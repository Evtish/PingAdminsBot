from typing import Callable
from aiogram.types import Message, User
from aiogram.utils import markdown

from time import time
from functools import wraps

from filters import proper_admin
from config import ADMIN_PING_TIMEOUT


def get_link_to_user(user: User) -> str:
    if user.username:
        return '@' + user.username
    else:
        return markdown.hlink(user.full_name, f"tg://user?id={user.id}")


async def get_admin_usernames(message: Message) -> list[str]:
    admin_usernames = []
    for cur_admin in await message.chat.get_administrators():
        if proper_admin(cur_admin, message):
            cur_admin_name = get_link_to_user(cur_admin.user)
            admin_usernames.append(cur_admin_name)
    return list(admin_usernames)


# controlling that bot messages are not too long
def split_long_text(text_list: list[str]) -> list[str]:
    MAX_MSG_LENGTH = 4096

    cur_message = ""
    msg_list = []
    for el in text_list:
        if len(cur_message) + len(el) <= MAX_MSG_LENGTH:
            cur_message += el + ' '
        else:
            msg_list.append(cur_message[:-1])
            cur_message = ""
    if cur_message:
        msg_list.append(cur_message[:-1])

    return msg_list


# decorator
def limit_command_frequency(func: Callable) -> Callable:
    last_call_time = time() - ADMIN_PING_TIMEOUT
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        nonlocal last_call_time
        deltaTime = time() - last_call_time

        if deltaTime >= ADMIN_PING_TIMEOUT:
            last_call_time = time()
            return await func(message, *args, **kwargs)

        else:
            await message.reply(
                f"Вы используете команду слишком часто. Попробуйте ещё раз через {round(ADMIN_PING_TIMEOUT - deltaTime, 2)} сек."
            )
    return wrapper


# decorator
def check_chat_type(*valid_types: tuple[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            if message.chat.type in valid_types:
                return await func(message, *args, **kwargs)
            else:
                await message.reply(f"Команда только для этих типов чатов: {", ".join(valid_types)}")
        return wrapper
    return decorator
