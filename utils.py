from aiogram.types import Message


#TODO: check admin type
def is_valid_admin(admin, message: Message) -> bool:
    excluded_admin_ids = {message.from_user.id, message.reply_to_message.from_user.id}
    return admin.user.id not in excluded_admin_ids and not admin.user.is_bot


async def get_admin_usernames(message: Message) -> list[str]:
    admin_usernames = []
    for cur_admin in await message.chat.get_administrators():
        if is_valid_admin(cur_admin, message):
            admin_usernames.append('@' + cur_admin.user.username)
    return list(admin_usernames)


def limit_msg_length(text_list: list[str]) -> list[str]:
    MAX_MSG_LENGTH = 4096

    cur_message = ''
    msg_list = []
    for el in text_list:
        if len(cur_message) + len(el) + 1 <= MAX_MSG_LENGTH:
            cur_message += el
        else:
            msg_list.append(cur_message)
            cur_message = ''

    return msg_list
