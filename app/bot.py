__all__ = ("main",)

from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app import callbacks, handlers, middlewares
from app.config import Config


async def main() -> None:
    bot_token: Optional[str] = Config.BOT_TOKEN

    if bot_token is None:
        exit("BOT_TOKEN is not set")

    storage = RedisStorage.from_url(Config.REDIS_URL)
    dp = Dispatcher(storage=storage)
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)

    dp.message.middleware(middlewares.throttling.ThrottlingMiddleware(0.5))

    dp.include_routers(
        handlers.start_command.router,
        handlers.help_command.router,
        handlers.menu_command.router,
        handlers.profile_command.router,
        handlers.create_travel_command.router,
        handlers.travels_command.router,
        callbacks.menu.router,
        callbacks.profile.router,
        callbacks.travel.router,
        callbacks.location.router,
        callbacks.notes.router,
        callbacks.fallback.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
