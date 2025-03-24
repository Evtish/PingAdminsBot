from aiogram import Router, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import Message, ChatMemberUpdated
from aiogram.utils import markdown

from typing import Callable

from utils import (
    get_admin_usernames,
    split_long_text,
    get_link_to_user,
    limit_command_frequency,
    check_chat_type
)

router = Router(name=__name__)

@router.message(Command("start", "help"))
async def send_info_msg(message: Message):
    await message.answer(
        "Привет! Этот бот отправляет в чат упоминания всех админов (кроме ботов). Чтобы сделать это, отправьте /admins. Это "
        "будет особенно полезно для блокировки подозрительных аккаунтов или рекламы, которую трудно распознать другим ботам. "
        "Об обнаруженных багах или по иным вопросам, связанным с этим ботом, писать сюда: @evevtish. Приятного пользования!"
    )


@router.message(Command("admins"))
@check_chat_type("group", "supergroup")
@limit_command_frequency
async def ping_admins(message: Message):
    message_texts = split_long_text(await get_admin_usernames(message))
    for text in message_texts:
        thread_fst_message = message.reply_to_message
        if thread_fst_message:
            await thread_fst_message.reply(text)
        else:
            await message.answer(text)


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    new_user = event.new_chat_member.user
    await event.answer(f"{markdown.hbold(new_user.full_name)} ({get_link_to_user(new_user)}) присоединился к {markdown.hunderline(event.chat.full_name)}!")
