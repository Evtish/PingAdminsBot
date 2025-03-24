from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message

from utils.filters import is_proper_admin


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


# TODO button to take on the conversation
async def answer_to_goy():
    pass