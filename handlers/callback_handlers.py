from utils.keyboard_utils import get_callback_items

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

callback_router = Router(name=__name__)


# @callback_router.callback_query(F.data.startswith("action_"))
# async def cancel_action(call: CallbackQuery, state: FSMContext):
#     await call.answer()
#     operation = get_callback_items(call.data)[1]

#     if operation == "cancel":
#         if await state.get_state() is None:
#             await call.message.reply("Отменять нечего")
#             return

#         await state.clear()
#         await call.message.edit_text(markdown.hstrikethrough(call.message.text) + "\n⛔️Действие было отменено⛔️")
#         # await call.message.reply("Действие было отменено")