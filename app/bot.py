__all__ = ("main",)

from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage

from app.callbacks import profile
from app.config import Config
from app.handlers import help_command, profile_command, start_command
from app.middlewares.throttling import ThrottlingMiddleware


async def main() -> None:
    bot_token: Optional[str] = Config.BOT_TOKEN

    if bot_token is None:
        exit("BOT_TOKEN is not set")

    storage = RedisStorage.from_url(Config.REDIS_URL)
    dp = Dispatcher(storage=storage)
    bot = Bot(bot_token, parse_mode=ParseMode.HTML)

    dp.message.middleware(ThrottlingMiddleware(0.5))
    # type: ignore
    dp.include_routers(
        start_command.router,
        profile_command.router,
        profile.router,  # type: ignore
        help_command.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
