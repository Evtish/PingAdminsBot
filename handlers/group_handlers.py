from aiogram.utils import markdown
from utils.decorator_utils import check_chat_type, limit_command_frequency
from utils.base_utils import get_admin_usernames, get_link_to_user, split_long_text

from aiogram import Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
from aiogram.types import ChatMemberUpdated, Message

group_router = Router(name=__name__)


@group_router.message(Command("admins"))
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


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# @group_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
# async def on_user_join(event: ChatMemberUpdated):
#     new_user = event.new_chat_member.user
#     # TODO restrict name length
#     # TODO split long text
#     # TODO add useful links, etc.
#     await event.answer(
#         f"{markdown.hbold(new_user.full_name)} ({get_link_to_user(new_user)}) присоединился к "
#         f"{markdown.hunderline(event.chat.full_name)}, добро пожаловать!\nПеред началом общения "
#         f"не забудьте ознакомиться с {markdown.hlink('правилами', 'https://t.me/clubnds/60944/705865')} нашего чата"
#     )

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!