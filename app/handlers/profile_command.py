__all__ = ("router",)

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from app.filters.user import Registered
from app.keyboards.profile import get
from app.models.user import User


router = Router(name="profile_command")


@router.message(Command("profile"), Registered(), StateFilter(None))
async def command_profile_handler(message: Message) -> None:
    if message.from_user is None:
        return

    user = User().get_user_by_telegram_id(message.from_user.id)

    await message.answer(
        user.get_profile_text(),
        reply_markup=get(),
    )
