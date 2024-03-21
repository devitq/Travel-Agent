__all__ = ()

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app import messages
from app.filters.user import Registered
from app.keyboards.profile import get
from app.models.user import User


router = Router(name="profile_command")


@router.message(Command("profile"), Registered())
async def command_profile_handler(message: Message) -> None:
    if message.from_user is None:
        return

    user = User().get_user_by_telegram_id(message.from_user.id)

    await message.answer(
        messages.PROFILE.format(
            username=user.username,
            age=user.age,
            bio=user.bio if user.bio else messages.NOT_SET,
            sex=user.sex.capitalize(),
            country=user.country,
            city=user.city,
        ),
        reply_markup=get(),
    )
