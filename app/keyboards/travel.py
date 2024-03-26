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
            text="📝 Change title",
            callback_data=f"travel_change_{travel.id}_title",
        ),
        types.InlineKeyboardButton(
            text="ℹ️ Change description",
            callback_data=f"travel_change_{travel.id}_description",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="🗺️ Locations",
            callback_data=f"travel_locations_page_{travel.id}_0",
        ),
        types.InlineKeyboardButton(
            text="➕ Add location",
            callback_data=f"travel_add_location_{travel.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="👤 Users",
            callback_data=f"travel_users_page_{travel.id}_0",
        ),
        types.InlineKeyboardButton(
            text="➕ Add user",
            callback_data=f"travel_add_user_{travel.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📝 Notes",
            callback_data=f"travel_notes_page_{travel.id}_0",
        ),
        types.InlineKeyboardButton(
            text="➕ Add note",
            callback_data=f"travel_add_note_{travel.id}",
        ),
    )
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
            text="❌ Delete travel",
            callback_data=f"travel_delete_{travel.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data="travels",
        ),
    )

    return builder.as_markup()


def get_public(travel: Travel):
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
            text="🗺️ Locations",
            callback_data=f"travel_locations_{travel.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="👤 Users",
            callback_data=f"travel_users_{travel.id}",
        ),
    )
    builder.row(
        types.InlineKeyboardButton(
            text="📝 Notes",
            callback_data=f"travel_notes_{travel.id}",
        ),
        types.InlineKeyboardButton(
            text="➕ Add note",
            callback_data=f"travel_add_note_{travel.id}",
        ),
    )
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
            callback_data="travels",
        ),
    )

    return builder.as_markup()
