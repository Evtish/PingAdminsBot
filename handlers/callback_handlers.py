from config import KB_BUTTONS, BotStates
from utils.keyboard_utils import build_inline_kb_markup, get_callback_items


from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

callback_router = Router(name=__name__)


@callback_router.callback_query(F.data.startswith("action_"))
async def cancel_action(call: CallbackQuery, state: FSMContext):
    await call.answer()
    operation = get_callback_items(call.data)[1]

    if operation == "cancel":
        if await state.get_state() is None:
            await call.message.reply("Отменять нечего")
            return

        await state.clear()
        await call.message.edit_text(markdown.hstrikethrough(call.message.text) + "\n⛔️Действие было отменено⛔️")
        # await call.message.reply("Действие было отменено")


# TODO split the file into several ones


@callback_router.callback_query(F.data.startswith("thread_"))
async def manage_thread(call: CallbackQuery, state: FSMContext):
    await call.answer("шары валеры", show_alert=False)
    is_thread_accepted, thread_author_id = map(int, get_callback_items(call.data)[1:])
    if is_thread_accepted:
        await call.message.reply(
            "Теперь вы будете вести этот диалог. Напишите ваш ответ",
            reply_markup=build_inline_kb_markup(call.message, KB_BUTTONS["action_management"])
        )
        await state.set_state(BotStates.ACCEPT_THREAD)
        await state.update_data(thread_author_id=thread_author_id)
    else:
        await call.message.reply(
            "Диалог отклонён",
            reply_markup=build_inline_kb_markup(call.message, KB_BUTTONS["action_management"])
        )
        await state.set_state(BotStates.DECLINE_THREAD)
    # await call.message.edit_text(call.message.text)