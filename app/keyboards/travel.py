__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get(travel_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="📝 Change title",
            callback_data=f"travel_change_{travel_id}_title",
        ),
        types.InlineKeyboardButton(
            text="ℹ️ Change description",
            callback_data=f"travel_change_{travel_id}_description",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="➕ Add location",
            callback_data=f"travel_add_{travel_id}_location",
        ),
        types.InlineKeyboardButton(
            text="➕ Add user",
            callback_data=f"travel_add_{travel_id}_user",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data="menu_travels",
        ),
    )

    return builder.as_markup()
