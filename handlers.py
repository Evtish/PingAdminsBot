from aiogram import Router, F
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.types import Message, ChatMemberUpdated
from aiogram.utils import markdown

from config import bot
from utils import get_admin_usernames, split_long_text

router = Router(name=__name__)


@router.message(Command("start", "help"))
async def send_info_msg(message: Message):
    await message.answer("Hi! This bot mentions all chat admins (except bots). To do this send /ping. It would be "
                         "especially helpful for blocking suspicious accounts or ads that are hard for other bots to "
                         "detect.\nFor found bugs or others issues with this bot, message here: @evevtish. Enjoy your "
                         "use!")


@router.message(Command("ping"))
async def ping_admins(message: Message):
    if message.chat.type in ("group", "supergroup"):
        message_texts = split_long_text(await get_admin_usernames(message))
        for text in message_texts:
            thread_fst_message = message.reply_to_message
            if thread_fst_message:
                await thread_fst_message.reply(text)
            else:
                await message.answer(text)
    else:
        await message.reply("This command is for groups and supergroups only.")


"""
@router.message(F.contains())
@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    new_user = event.new_chat_member.user
    await event.answer(markdown.hlink(new_user.full_name, new_user.username))
    await bot.delete_message(event.chat.id, event.)
"""
