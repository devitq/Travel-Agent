__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="Yes",
            callback_data="confirm_location",
        ),
        types.InlineKeyboardButton(text="No", callback_data="cancel_location"),
    )

    return builder.as_markup()
