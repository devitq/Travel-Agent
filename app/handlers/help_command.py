__all__ = ("router",)

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from app import messages
from app.filters.user import Registered


router = Router(name="help_command")


@router.message(Command("help"), Registered(), StateFilter(None))
async def command_help_handler(message: Message) -> None:
    await message.answer(messages.HELP_MESSAGE)
