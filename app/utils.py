from aiogram import Bot
from aiogram.types import Message, User
from aiogram.utils import markdown
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from time import time
from functools import wraps
from typing import Callable

from filters import is_proper_admin
from config import ADMIN_PING_TIMEOUT


def get_link_to_user(user: User) -> str:
    if user.username:
        return '@' + user.username
    else:
        return markdown.hlink(user.full_name, f"tg://user?id={user.id}")


async def get_admin_usernames(message: Message) -> list[str]:
    admin_usernames = []
    for cur_admin in await message.chat.get_administrators():
        if is_proper_admin(cur_admin, message):
            cur_admin_name = get_link_to_user(cur_admin.user)
            admin_usernames.append(cur_admin_name)
    return list(admin_usernames)


# TODO change parameter: list[str] -> str 
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


# async def notify_admins(text: str, chat_id: int | str, bot: Bot):
#     for cur_admin in await bot.get_chat_administrators(chat_id):
#         print(cur_admin.user.username)
#         await bot.send_message(cur_admin.user.id, text)


async def forward_to_admins(message: Message, group_id: int | str, bot: Bot, additional_text: str = None):
    error_code = 0

    for cur_admin in await bot.get_chat_administrators(group_id):
        print(error_code)
        try:
            if is_proper_admin(cur_admin, message):
                if additional_text:
                    await bot.send_message(cur_admin.user.id, additional_text)
                await message.forward(cur_admin.user.id)

            #-----------------------------
            # print(cur_admin.user.username)
            #-----------------------------
        except TelegramBadRequest:
            error_code = 1
        except TelegramForbiddenError:
            error_code = 2

    match error_code:
        case 0:
            await message.answer("Ваше сообщение было успешно отправлено всем админам")
        case 1:
            await message.answer("Ошибка при отправке сообщения: чат не найдет")
        case 2:
            await message.answer("Сообщение дошло не до всех админов. Кто-то из них не начал диалог с ботом")
        


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
                f"Вы используете команду слишком часто. Попробуйте ещё раз через {round(ADMIN_PING_TIMEOUT - deltaTime, 1)} сек."
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
