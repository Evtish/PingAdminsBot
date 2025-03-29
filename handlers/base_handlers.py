from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

base_router = Router(name=__name__)


@base_router.message(Command("start", "help"))
async def send_info_msg(message: Message):
    await message.answer(
        "Привет! Этот бот отправляет в чат упоминания всех админов (кроме ботов). Чтобы сделать это, отправьте /admins. Это "
        "будет особенно полезно для блокировки подозрительных аккаунтов или рекламы, которую трудно распознать другим ботам. "
        "Об обнаруженных багах или по иным вопросам, связанным с этим ботом, писать сюда: t.me/evevtish. Приятного пользования!",
        link_preview_options={"is_disabled": True}
    )


# @base_router.message()
# async def set(message: Message):
#     print((await bot.get_chat(TARGET_CHAT_ID)).full_name)
#     for cur_admin in await bot.get_chat_administrators(TARGET_CHAT_ID):
#         print(cur_admin.user.username)