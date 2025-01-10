from aiogram.filters import Command
from aiogram.types import Message

from main import dp
from utils import get_admin_usernames, split_long_text


@dp.message(Command("start", "help"))
async def send_info_msg(message: Message):
    await message.answer("""Hi! This bot mentions all admins (except bots).
    This would be especially helpful for blocking suspicious accounts or ads that are hard for other bots to detect.
    For found bugs or others issues with this bot, message here: @evevtish.
    Enjoy your use!
    
    Привет! Этот бот отправляет в чат упоминания всех админов (кроме ботов).
    Это будет особенно полезен для блокировки подозрительных аккаунтов или рекламы, которую трудно распознать другим ботам.
    Об обнаруженных багах или по иным вопросам, связанным с этим ботом, писать сюда: @evevtish.
    Приятного пользования!""")


@dp.message(Command("ping"))
async def ping_admins(message: Message) -> None:
    message_texts = split_long_text(await get_admin_usernames(message))
    for text in message_texts:
        await message.reply_to_message.reply(text, allow_sending_without_reply=True)