from config import KB_BUTTONS, BotStates
from utils.decorators import check_chat_type
from utils.keyboard_utils import build_inline_kb_markup


from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

threading_router = Router(name=__name__)


@threading_router.message(Command("new_thread"))
@check_chat_type("private")
async def handle_creating_new_thread(message: Message, state: FSMContext):
    bot_replying_message = await message.answer(
        "Напишите ваш вопрос к администрации",
        reply_markup=build_inline_kb_markup(message, KB_BUTTONS["action_management"])
    )
    await state.set_state(BotStates.CREATE_NEW_THREAD)

    # TODO delete cancel button when action is performed
    # TODO class for messages with the cancel button and the button deleting method
    # await state.update_data(bot_replying_message_id = bot_replying_message.id)