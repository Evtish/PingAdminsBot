from aiogram.types import Message

from time import time
from functools import wraps
from typing import Callable

from config import ADMIN_PING_TIMEOUT


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