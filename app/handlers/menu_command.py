__all__ = ()

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from app import messages
from app.filters.user import Registered
from app.keyboards.menu import get


router = Router(name="menu_command")


@router.message(Command("menu"), Registered(), StateFilter(None))
async def command_menu_handler(message: Message) -> None:
    await message.answer(messages.MENU, reply_markup=get())
