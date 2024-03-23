__all__ = ("main",)

from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.callbacks import menu, profile, travels
from app.config import Config
from app.handlers import (
    create_travel_command,
    help_command,
    menu_command,
    profile_command,
    start_command,
    travels_command,
)
from app.middlewares.throttling import ThrottlingMiddleware


async def main() -> None:
    bot_token: Optional[str] = Config.BOT_TOKEN

    if bot_token is None:
        exit("BOT_TOKEN is not set")

    storage = RedisStorage.from_url(Config.REDIS_URL)
    dp = Dispatcher(storage=storage)
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)

    dp.message.middleware(ThrottlingMiddleware(0.5))

    dp.include_routers(
        start_command.router,
        help_command.router,
        menu_command.router,
        profile_command.router,
        create_travel_command.router,
        travels_command.router,
        menu.router,
        profile.router,
        travels.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
