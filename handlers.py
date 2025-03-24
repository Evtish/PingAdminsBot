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
    await message.answer("Hi! This bot mentions all chat admins (except bots). To do this send /admins. It would be "
                         "especially helpful for blocking suspicious accounts or ads that are hard for other bots to "
                         "detect.\nFor found bugs or others issues with this bot, message here: @evevtish. Enjoy your "
                         "use!")


"""
@router.message(Command("admins"))
async def ping_admins(message: Message):
    async def create_ping_helper(msg: Message) -> Callable:
        last_call_time = time()

        async def wrapper():
            if message.chat.type in ("group", "supergroup"):
                print(time() - last_call_time)

                if timeout_passed(last_call_time, ADMIN_PING_TIMEOUT):
                    message_texts = split_long_text(await get_admin_usernames(message))
                    for text in message_texts:
                        thread_fst_message = message.reply_to_message
                        if thread_fst_message:
                            await thread_fst_message.reply(text)
                        else:
                            await message.answer(text)
                    nonlocal last_call_time
                    last_call_time = time()
                else:
                    await message.reply(f"You\'re calling the command too often. Try again in {time() - last_call_time} seconds")
            else:
                await message.reply("This command is for groups and supergroups only")
        return wrapper
    
    ping_helper = await create_ping_helper(message)
    await ping_helper()
"""


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


# @router.message(F.contains())
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    new_user = event.new_chat_member.user
    await event.answer(f"{markdown.hbold(new_user.full_name)} ({get_link_to_user(new_user)}) has joined {markdown.hunderline(event.chat.full_name)}!")
    # await bot.delete_message(event.chat.id, event.)
