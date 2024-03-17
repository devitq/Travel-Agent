__all__ = ("main",)

from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from app.config import Config


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def echo_handler(message: types.Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot_token: Optional[str] = Config.BOT_TOKEN
    if bot_token is not None:
        bot = Bot(bot_token, parse_mode=ParseMode.HTML)
        await dp.start_polling(bot)
    else:
        exit("BOT_TOKEN is not set")
