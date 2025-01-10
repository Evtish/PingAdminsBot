from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils import get_admin_usernames, split_long_text

handler_router = Router(name=__name__)


@handler_router.message(Command("start", "help"))
async def send_info_msg(message: Message) -> None:
    await message.answer("Hi! This bot mentions all admins (except bots). This would be especially helpful for "
                         "blocking suspicious accounts or ads that are hard for other bots to detect.\nFor found bugs "
                         "or others issues with this bot, message here: @evevtish. Enjoy your use!\n\nПривет! Этот "
                         "бот отправляет в чат упоминания всех админов (кроме ботов). Это будет особенно полезен для "
                         "блокировки подозрительных аккаунтов или рекламы, которую трудно распознать другим ботам.\n"
                         "Об обнаруженных багах или по иным вопросам, связанным с этим ботом, писать сюда: @evevtish. "
                         "Приятного пользования!")


@handler_router.message(Command("ping"))
async def ping_admins(message: Message) -> None:
    if message.chat.type in ("group", "supergroup"):
        message_texts = split_long_text(await get_admin_usernames(message))
        for text in message_texts:
            thread_fst_message = message.reply_to_message
            if thread_fst_message:
                await thread_fst_message.reply(text)
            else:
                await message.answer(text)
    else:
        await message.reply("This command is for groups and supergroups only.\n\nЭта команда предназначена только для "
                            "групп и супергрупп.")