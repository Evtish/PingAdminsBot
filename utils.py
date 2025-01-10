from aiogram.types import Message, ChatMemberAdministrator


# admin must be:
# not bot, command sender or original message author
# able to delete messages, restrict or ban members
def is_proper_admin(admin: ChatMemberAdministrator, message: Message) -> bool:
    excluded_admin_ids = {message.from_user.id}
    thread_fst_message = message.reply_to_message
    if thread_fst_message:
        excluded_admin_ids.add(thread_fst_message.from_user.id)

    try:
        return (admin.user.id not in excluded_admin_ids
                and
                not admin.user.is_bot
                and
                (admin.can_delete_messages or admin.can_restrict_members))
    except AttributeError:
        return True


async def get_admin_usernames(message: Message) -> list[str]:
    admin_usernames = []
    for cur_admin in await message.chat.get_administrators():
        if is_proper_admin(cur_admin, message):
            admin_usernames.append('@' + cur_admin.user.username)
    return list(admin_usernames)


# controlling that bot messages are not too long
def split_long_text(text_list: list[str]) -> list[str]:
    MAX_MSG_LENGTH = 4096

    cur_message = ''
    msg_list = []
    for el in text_list:
        if len(cur_message) + len(el) <= MAX_MSG_LENGTH:
            cur_message += el + ' '
        else:
            msg_list.append(cur_message[:-1])
            cur_message = ''
    if cur_message:
        msg_list.append(cur_message[:-1])

    return msg_list
