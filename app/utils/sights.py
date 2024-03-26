__all__ = ("find_trips", "get_info_by_xid")

from aiogram.types import CallbackQuery, Message
import requests

from app import messages
from app.config import Config


def find_trips(lat, lon, type_of_trip="unclassified_objects"):
    api_key = Config.OPENTRIPMAP_API_KEY
    radius = Config.NEARBY_SIGHTS_RADIUS

    result_url = (
        "https://api.opentripmap.com/0.1/ru/places/radius"
        f"?radius={radius}&"
        f"kinds={type_of_trip}&"
        f"lon={lon}&"
        f"lat={lat}&"
        f"limit=20&"
        f"apikey={api_key}"
    )

    data = requests.get(result_url).json()

    if data["features"]:
        sights = []

        for feature in data["features"]:
            button_text = (
                feature["properties"]["name"]
                + " ("
                + str(round(feature["properties"]["dist"]))
                + "m)"
            )

            sights.append((button_text, feature["properties"]["xid"]))

        return sights

    return None


async def get_info_by_xid(callback: CallbackQuery, xid):
    if not isinstance(callback.message, Message):
        return

    api_key = Config.OPENTRIPMAP_API_KEY

    result_url = (
        f"https://api.opentripmap.com/0.1/ru/places/xid/{xid}?apikey={api_key}"
    )

    data = requests.get(result_url).json()

    text = messages.SIGHT_DETAIL

    if data.get("name", ""):
        text += (
            "\n\t<b>📝 Name:</b> " + data.get("name", "<i>Missing</i>") + "\n"
        )

    if data.get("address", ""):
        address_string = ""
        key_order = [
            "country",
            "state",
            "city",
            "city_district",
            "suburb",
            "road",
            "house_number",
        ]
        address = data["address"]

        for key in key_order:
            if address.get(key, ""):
                address_string += f" {address.get(key)}, "

        text += "\t<b>📫 Address:</b> " + address_string + "\n"

    if "wikipedia_extracts" in data:
        wikipedia_extracts = data["wikipedia_extracts"]
        wikipedia_title = wikipedia_extracts.get("title", "<i>Missing</i>")
        wikipedia_description = wikipedia_extracts.get(
            "text",
            "<i>Missing</i>",
        )

        text += f"\n\t<b>📝 Wikipedia title:</b> {wikipedia_title}\n"
        text += f"\t<b>ℹ️ Wikipedia description:</b> {wikipedia_description}\n"

    if "wikipedia" in data:
        wikipedia_link = data["wikipedia"]

        text += f"\t<b>🔗 Wikipedia link:</b> {wikipedia_link}\n"

    if "image" in data:
        await callback.message.answer_photo(
            data["image"],
            text,
            reply_to_message_id=callback.message.message_id,
        )
    else:
        await callback.message.answer(
            text,
            reply_to_message_id=callback.message.message_id,
        )
