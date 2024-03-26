__all__ = ("Config",)

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///database.db",
    )
    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379",
    )
    OPENTRIPMAP_API_KEY = os.getenv(
        "OPENTRIPMAP_API_KEY",
    )
    OPENWEATHERMAP_API_KEY = os.getenv(
        "OPENWEATHERMAP_API_KEY",
    )
    NEARBY_SIGHTS_RADIUS = 2000
    PAGE_SIZE = 6
