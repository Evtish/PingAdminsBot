from aiogram import Bot, Router
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_MEMBER, IS_NOT_MEMBER
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ChatMemberUpdated
from aiogram.utils import markdown
# from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError

from config import BotStates, TARGET_CHAT_ID

from utils import (
    get_admin_usernames,
    split_long_text,
    get_link_to_user,
    forward_to_admins,
    limit_command_frequency,
    check_chat_type
)

router = Router(name=__name__)

# @router.message()
# async def set(message: Message):
#     print((await bot.get_chat(TARGET_CHAT_ID)).full_name)
#     for cur_admin in await bot.get_chat_administrators(TARGET_CHAT_ID):
#         print(cur_admin.user.username)

@router.message(Command("start", "help"))
async def send_info_msg(message: Message):
    # TODO add useful links, etc.
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
    # TODO restrict name length
    # TODO split long text
    await event.answer(split_long_text(
        f"{markdown.hbold(new_user.full_name)} ({get_link_to_user(new_user)}) присоединился к {markdown.hunderline(event.chat.full_name)}!"
    ))


@check_chat_type("private")
@router.message(Command("new_thread"))
async def handle_creating_new_thread(message: Message, state: FSMContext):
    await state.set_state(BotStates.CREATE_NEW_THREAD)
    await message.answer("Напишите ваш вопрос к администрации")

@router.message(BotStates.CREATE_NEW_THREAD)
async def create_new_thread(message: Message, state: FSMContext, bot: Bot):
    # TODO split long text
    mailing_prefix = markdown.hitalic(f"Сообщение от {get_link_to_user(message.from_user)}:")
    await state.set_state(BotStates.BASIC_STATE)
    await forward_to_admins(message, TARGET_CHAT_ID, bot, additional_text=mailing_prefix)
    # try:
    #     await forward_to_admins(message, TARGET_CHAT_ID, bot, additional_text=mailing_prefix)
    #     await message.answer("Ваше сообщение было успешно отправлено всем админам")
    # except TelegramForbiddenError:
    #     await message.answer("Сообщение дошло не до всех админов. Кто-то из них не начал диалог с ботом")
    # except TelegramBadRequest:
    #     await message.answer("Ошибка при отправке сообщения: чат не найдет")
