__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get():
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="👤 Change username",
            callback_data="profile_change_username",
        ),
        types.InlineKeyboardButton(
            text="🔢 Change age",
            callback_data="profile_change_age",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="ℹ️ Change bio",
            callback_data="profile_change_bio",
        ),
        types.InlineKeyboardButton(
            text="📝 Change sex",
            callback_data="profile_change_sex",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗺️ Change location",
            callback_data="profile_change_location",
        ),
    )

    return builder.as_markup()
