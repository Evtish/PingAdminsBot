from aiogram import Bot, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.utils import markdown
from config import TARGET_CHAT_ID, BotStates
from utils.threading_utils import forward_to_admins

fsm_router = Router(name=__name__)


@fsm_router.message(BotStates.CREATE_NEW_THREAD)
async def create_new_thread(message: Message, state: FSMContext, bot: Bot):
    # TODO split long text
    await forward_to_admins(message, TARGET_CHAT_ID, bot)  # , additional_text=mailing_prefix)
    await state.clear()


@fsm_router.message(BotStates.ACCEPT_THREAD)
async def answer_in_thread(message: Message, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    await bot.send_message(state_data["thread_author_id"], markdown.hitalic("Новое сообщение от администрации:\n\n") + message.text)
    await message.answer("Ваш ответ был успешно доставлен")
    await state.clear()