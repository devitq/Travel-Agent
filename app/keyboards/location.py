__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get(travel_id: int, location_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="⏩ Get nearby sights",
            callback_data=f"travel_locationsights_{location_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="☁️ Current weather",
            callback_data=f"travel_locationweather_{location_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="❌ Delete location",
            callback_data=f"travel_locationdelete_{location_id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_locations_page_{travel_id}_0",
        ),
    )

    return builder.as_markup()


def get_public(travel_id: int, location_id: int):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_locations_page_{travel_id}_0",
        ),
    )

    return builder.as_markup()
