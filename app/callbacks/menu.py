# type: ignore
__all__ = ()

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery

from app import messages
from app.filters.user import RegisteredCallback
from app.keyboards.profile import get
from app.models.user import User


router = Router(name="menu_callback")


@router.callback_query(F.data == "menu_profile", RegisteredCallback())
async def profile_callback(callback: CallbackQuery) -> None:
    if callback.data is None or callback.message is None:
        return

    user = User().get_user_by_telegram_id(callback.from_user.id)

    await callback.message.answer(
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
    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass
