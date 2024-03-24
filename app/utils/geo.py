# type: ignore
__all__ = ("validate_country", "validate_city", "get_location_by_name")

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


def validate_country(country: str):
    geolocator = Nominatim(user_agent="travel_agent_bot")

    for _ in range(3):
        try:
            geocode = geolocator.geocode(
                country,
                featuretype="country",
            )
            break
        except GeocoderTimedOut:
            continue
    else:
        return False, None

    if not geocode:
        return False, None

    is_loc_country = (
        geocode.raw.get(
            "type",
            None,
        )
        == "administrative"
    )

    if is_loc_country:
        normalized_country = geocode.raw.get("name", "Invalid country")
        return True, normalized_country

    return False, None


def validate_city(city: str, country: str):
    geolocator = Nominatim(user_agent="travel_agent_bot")

    location_name = f"{country}, {city}"
    valid_list = ["city", "town", "administrative"]

    for _ in range(3):
        try:
            geocode = geolocator.geocode(
                location_name,
                featuretype="city",
            )
            break
        except GeocoderTimedOut:
            continue
    else:
        return False, None

    if not geocode:
        return False, None

    check_in_valid = (
        geocode.raw.get(
            "type",
            None,
        )
        in valid_list
    )

    if geocode and check_in_valid:
        normalized_country = geocode.raw.get("name", "Invalid city")
        return True, normalized_country

    return False, None


def get_location_by_name(location: str) -> None:
    geolocator = Nominatim(user_agent="travel_agent_bot")

    for _ in range(3):
        try:
            geocode = geolocator.geocode(
                location,
                featuretype="city",
            )
            break
        except GeocoderTimedOut:
            continue
    else:
        return False, None

    if not geocode:
        return False, None

    return True, geocode
