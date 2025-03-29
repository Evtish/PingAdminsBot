from aiogram.types import Message, User
from aiogram.utils import markdown

from utils.filters import is_proper_admin


def get_link_to_user(user: User) -> str:
    if user.username:
        return '@' + user.username
    else:
        return markdown.hlink(user.full_name, f"tg://user?id={user.id}")


async def get_admin_usernames(message: Message) -> list[str]:
    admin_usernames = []
    for cur_admin in await message.chat.get_administrators():
        print(cur_admin.user.username)
        if is_proper_admin(cur_admin, message):
            cur_admin_name = get_link_to_user(cur_admin.user)
            admin_usernames.append(cur_admin_name)
    return list(admin_usernames)


# TODO change parameter: list[str] -> str 
# controlling that bot messages are not too long
def split_long_text(text_list: list[str]) -> list[str]:
    MAX_MSG_LENGTH = 4096

    cur_message = ""
    msg_list = []
    for el in text_list:
        if len(cur_message) + len(el) <= MAX_MSG_LENGTH:
            cur_message += el + ' '
        else:
            msg_list.append(cur_message[:-1])
            cur_message = ""
    if cur_message:
        msg_list.append(cur_message[:-1])

    return msg_list
