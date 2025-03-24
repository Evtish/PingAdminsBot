from aiogram.types import ChatMemberAdministrator, Message


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
                (admin.can_delete_messages or admin.can_restrict_members))
    except AttributeError:
        return True
