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
            text="🗺️ Locations",
            callback_data=f"travel_locations_{travel_id}",
        ),
        types.InlineKeyboardButton(
            text="➕ Add location",
            callback_data=f"travel_add_location_{travel_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="👤 Users",
            callback_data=f"travel_users_{travel_id}",
        ),
        types.InlineKeyboardButton(
            text="➕ Add user",
            callback_data=f"travel_add_user_{travel_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📝 Notes",
            callback_data=f"travel_notes_{travel_id}",
        ),
        types.InlineKeyboardButton(
            text="➕ Add note",
            callback_data=f"travel_add_note_{travel_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="❌ Delete travel",
            callback_data=f"travel_delete_{travel_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data="travels",
        ),
    )

    return builder.as_markup()
