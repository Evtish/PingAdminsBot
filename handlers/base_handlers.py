from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils import markdown

base_router = Router(name=__name__)

@base_router.message(Command("cancel"))
async def handle_cancel(message: Message, state: FSMContext):
    if await state.get_state():
        await state.clear()
        await message.answer("⛔️ Действие отменено")
    else:
        await message.answer("Отменять нечего")


@base_router.message(Command("start"))
async def send_info_msg(message: Message):
    await message.answer(
        f"Привет! Это Bridge, бот для {markdown.hbold('управления сетью ваших сообществ')}.\n\nЕго функционал:\n"
        f"• {markdown.hbold('Упоминание всех админов')}. Это будет особенно полезно для блокировки подозрительных "
        "аккаунтов или рекламы, которую трудно распознать другим ботам.\n\n"
        f"• Отправка {markdown.hbold('приветственного сообщения')} всем новичкам в группе. Например, с правилами вашего сообщества\n\n"
        f"• {markdown.hbold('Связь участников с администрацией')}. Это позволяет равномерно распределять работу по обратной связи на всю "
        "администрацию и организовать общение для разных сообществ, которыми вы владеете, в одном месте\n\n"
        "Об обнаруженных багах или по иным вопросам, связанным с этим ботом, писать сюда: t.me/evevtish. Приятного пользования!",
        link_preview_options={"is_disabled": True}
    )


@base_router.message(Command("help"))
async def send_help_msg(message: Message):
    await message.answer(
        "Список команд:\n"
        "• /start — стартовое сообщение\n"
        "• /help — это сообщение\n"
        "• /admins — упоминание всех админов в сообщении (только для групп)\n"
        "• /new_thread — создать новый диалог с администрацией (только для ЛС)\n"
        "• /cancel — отменить текущее действие\n\n"
        "Остальной функционал, например, приветственное сообщение для новичков в сообществе "
        "или ограничение частоты вызова команд, происходит автоматически"
    )