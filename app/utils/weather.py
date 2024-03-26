__all__ = "get_weather"

import requests

from app.config import Config


def get_current_weather(lat, lot):
    api_key = Config.OPENWEATHERMAP_API_KEY
    result_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lot}&appid={api_key}&lang=en&units=metric"  # noqa

    return requests.get(result_url).json()
