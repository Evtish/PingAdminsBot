from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

DIVIDER = "_"


def build_inline_kb_markup(message: Message, buttons: dict[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for btn_callback, btn_text in buttons.items():
        builder.button(text=btn_text, callback_data=btn_callback + DIVIDER + str(message.from_user.id))
    
    builder.adjust(2)

    return builder.as_markup()


def get_callback_items(callback_data: str) -> list[str]:
    return callback_data.split(DIVIDER)