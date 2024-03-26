__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="👤 Profile",
            callback_data="menu_profile",
        ),
        types.InlineKeyboardButton(
            text="➕ Create travel",
            callback_data="menu_create_travel",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📃 Travels",
            callback_data="menu_travels",
        ),
        types.InlineKeyboardButton(
            text="❓ Help",
            callback_data="menu_help",
        ),
    )

    return builder.as_markup()
