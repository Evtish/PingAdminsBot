from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message
from aiogram.utils import markdown

from utils.helpers import get_link_to_user
from utils.filters import is_proper_admin
from utils.keyboard_utils import build_inline_kb_markup
from config import KB_BUTTONS


async def forward_to_admins(thread_question_message: Message, group_id: int | str, bot: Bot):  # , additional_text: str = None):
    error_code = 0
    info_message = await thread_question_message.answer("⏳Произвожу отправку. Это может занять несколько секунд...")
    for cur_admin in await bot.get_chat_administrators(group_id):
        # print(error_code)
        try:
            # if is_proper_admin(cur_admin, message):
                # if additional_text:
                #     await bot.send_message(cur_admin.user.id, additional_text)
                await thread_question_message.forward(cur_admin.user.id)
                await bot.send_message(
                    cur_admin.user.id,
                    markdown.hitalic(f"👆Сообщение от {get_link_to_user(thread_question_message.from_user)}👆"),
                    reply_markup=build_inline_kb_markup(thread_question_message, KB_BUTTONS["thread_management"])
                )

                #-----------------------------
                print(cur_admin.user.username)
                #-----------------------------
        except TelegramBadRequest:
            error_code = 1
        except TelegramForbiddenError:
            error_code = 2

    match error_code:
        case 0:
            await info_message.edit_text("✅Ваше сообщение было успешно отправлено всем админам")
        case 1:
            await info_message.edit_text("❌Ошибка при отправке сообщения: исходная группа не найдена")
        case 2:
            await info_message.edit_text(
                "⚠️Сообщение было отправлено, но оно дошло не до всех админов. "
                "Вероятнее всего, кто-то из них не начал диалог с ботом"
            )


# TODO button to take on the conversation
# async def answer_to_goy():
#     pass