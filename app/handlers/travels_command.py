__all__ = ("router",)

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from app import messages
from app.config import Config
from app.filters.user import Registered
from app.keyboards.builders import travels_keyboard
from app.models.user import User


router = Router(name="travels_command")


@router.message(Command("travels"), Registered(), StateFilter(None))
async def command_travels_handler(message: Message) -> None:
    page = 0

    if message.from_user is None:
        return

    user = User().get_user_by_telegram_id(message.from_user.id)

    travels = user.get_user_travels()

    if not travels or travels == []:
        await message.answer(messages.NO_TRAVELS)
    else:
        pages = (len(travels) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

        await message.answer(
            messages.TRAVELS,
            reply_markup=travels_keyboard(
                travels,
                page,
                pages,
                user.telegram_id,
            ),
        )
