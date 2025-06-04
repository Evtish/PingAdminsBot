from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from utils.base_utils import get_link_to_user
from utils.filter_utils import is_proper_admin
from utils.keyboard_utils import build_inline_kb_markup

from config import KB_BUTTONS


async def forward_to_admins(
        thread_question_message: Message,
        group_id: int | str,
        bot: Bot,
    ) -> list[tuple[int]]:  # , additional_text: str = None):
    
    messages_admins_received = []
    cur_message = None
    error_code = 0
    info_message = await thread_question_message.answer("⏳ Произвожу отправку. Это может занять несколько секунд...")
    for cur_admin in await bot.get_chat_administrators(group_id):
        cur_admin_id = cur_admin.user.id
        # print(error_code)
        try:
            # if is_proper_admin(cur_admin, message):
                # if additional_text:
                #     await bot.send_message(cur_admin_id, additional_text)
                await thread_question_message.forward(cur_admin_id)
                cur_message = await bot.send_message(
                    cur_admin_id,
                    markdown.hitalic(f"👆 Сообщение от {get_link_to_user(thread_question_message.from_user)}"),
                    reply_markup=build_inline_kb_markup(thread_question_message, KB_BUTTONS["thread_management"])
                )
        except TelegramBadRequest:
            error_code = 1
        except TelegramForbiddenError:
            error_code = 2
        else:
            messages_admins_received.append((cur_message.message_id, cur_message.chat.id))
            #-----------------------------
            print(cur_admin.user.username)
            # print(cur_message.message_id)
            #-----------------------------

    match error_code:
        case 0:
            await info_message.edit_text("✅ Ваше сообщение было успешно отправлено всем админам")
        case 1:
            await info_message.edit_text("❌ Ошибка при отправке сообщения: исходная группа не найдена")
        case 2:
            await info_message.edit_text("⚠️ Сообщение было отправлено, но оно дошло не до всех админов. Вероятно, кто-то из них не запустил бота")
    
    return messages_admins_received


# TODO button to take on the conversation
# async def answer_to_goy():
#     pass