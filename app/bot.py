__all__ = ("main",)

from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.config import Config
from app.handlers import help_command, profile_command, start_command
from app.middlewares.throttling import ThrottlingMiddleware


async def main() -> None:
    dp = Dispatcher()

    bot_token: Optional[str] = Config.BOT_TOKEN
    if bot_token is not None:
        bot = Bot(bot_token, parse_mode=ParseMode.HTML)

        dp.message.middleware(ThrottlingMiddleware(0.5))
        dp.include_routers(
            start_command.router,
            profile_command.router,
            help_command.router,
        )

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    else:
        exit("BOT_TOKEN is not set")
