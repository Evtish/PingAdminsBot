from config import TARGET_CHAT_ID, KB_BUTTONS, BotStates

from utils.decorator_utils import check_chat_type
from utils.keyboard_utils import build_inline_kb_markup, get_callback_items
from utils.threading_utils import forward_to_admins

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown

threading_router = Router(name=__name__)


# ------------------------------ new thread was created ------------------------------ #
@threading_router.message(Command("new_thread"))
@check_chat_type("private")
async def handle_creating_new_thread(message: Message, state: FSMContext):
    bot_replying_message = await message.answer(
        "Напишите ваш вопрос к администрации. Имейте ввиду, что при отправке администрация увидит ваш профиль",
        # reply_markup=build_inline_kb_markup(message, KB_BUTTONS["action_management"])
    )
    await state.set_state(BotStates.CREATE_NEW_THREAD)

    # TODO delete cancel button when action is performed
    # TODO class for messages with the cancel button and the button deleting method
    # await state.update_data(bot_replying_message_id=bot_replying_message.id)


# ------------------------------ sending the message to admins ------------------------------ #
@threading_router.message(BotStates.CREATE_NEW_THREAD)
async def create_new_thread(message: Message, state: FSMContext, bot: Bot):
    # TODO split long text
    # TODO ? restrict sending of commands ?
    messages_admins_received = await forward_to_admins(message, TARGET_CHAT_ID, bot)  # , additional_text=mailing_prefix)
    await state.clear()
    await state.update_data(messages_admins_received=messages_admins_received)


# ------------------------------ process message accepting/declining by an admin ------------------------------ #
@threading_router.callback_query(F.data.startswith("thread_"))
async def manage_thread(call: CallbackQuery, state: FSMContext, bot: Bot):
    await call.answer()
    thread_is_accepted, thread_author_id = map(int, get_callback_items(call.data)[1:3])
    # received_messages: list[tuple[int]] = (await state.get_data())["messages_admins_received"]

    if thread_is_accepted:
        # edit messages, delete keyboards
        # updated_msg_text = call.message.text + "\n\nℹ️ Этот диалог "
        # for message_data in received_messages:
        #     message_id, message_chat_id = message_data
        #     if message_chat_id == call.message.chat.id:
        #         await bot.edit_message_text(
        #             text=updated_msg_text + f"ведёте вы. {markdown.hbold('Напишите ваш ответ!')}",
        #             chat_id=message_chat_id,
        #             message_id=message_id
        #         )
        #     else:
        #         await bot.edit_message_text(
        #             text=updated_msg_text + "уже взял кто-то другой",
        #             chat_id=message_chat_id,
        #             message_id=message_id
        #         )

        # write in db
        # ...

        await call.message.reply(
            "Напишите ваш ответ",
            # reply_markup=build_inline_kb_markup(call.message, KB_BUTTONS["action_management"])
        )
        await state.set_state(BotStates.ACCEPT_THREAD)
        await state.update_data(thread_author_id=thread_author_id)
    else:
        await call.message.reply(
            "Диалог отклонён",
            # reply_markup=build_inline_kb_markup(call.message, KB_BUTTONS["action_management"])
        )
        await state.set_state(BotStates.DECLINE_THREAD)
    # await call.message.edit_text(call.message.text)


# ------------------------------ send the admin answer to thread creator ------------------------------ #
@threading_router.message(BotStates.ACCEPT_THREAD)
async def answer_in_thread(message: Message, state: FSMContext, bot: Bot):
    thread_author_id = (await state.get_data())["thread_author_id"]
    await message.copy_to(thread_author_id)
    await bot.send_message(thread_author_id, markdown.hitalic("👆 Ответ от администрации"))
    await message.answer("Ваш ответ был успешно доставлен")
    await state.clear()