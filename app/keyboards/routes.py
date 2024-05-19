__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.models.travel import Travel
from app.utils.geo import get_location_by_name
from app.utils.map import get_url_map


def get(travel: Travel):
    locations = Travel().get_sorted_locations(travel, asc=False)
    coordinats = []

    for location in locations:
        geocode = get_location_by_name(location.location)
        coordinats.append(
            [geocode[1].raw.get("lat"), geocode[1].raw.get("lon")],
        )

    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="🗺️ Route by car",
            web_app=types.WebAppInfo(
                url=get_url_map(
                    coordinats=coordinats,
                    profile="car",
                ),
            ),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗺️ Route on foot",
            web_app=types.WebAppInfo(
                url=get_url_map(
                    coordinats=coordinats,
                    profile="foot",
                ),
            ),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗺️ Route by bike",
            web_app=types.WebAppInfo(
                url=get_url_map(
                    coordinats=coordinats,
                    profile="bike",
                ),
            ),
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_detail_{travel.id}",
        ),
    )

    return builder.as_markup()
