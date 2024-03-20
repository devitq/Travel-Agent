__all__ = ()

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import messages
from app.filters.user_filter import Registered


router = Router(name="help_command")


@router.message(Command("help"), Registered())
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP_MESSAGE)
