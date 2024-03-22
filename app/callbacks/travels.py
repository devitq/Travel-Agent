# type: ignore
__all__ = ()

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

from app import messages
from app.config import Config
from app.filters.user import RegisteredCallback
from app.keyboards.builders import travels_keyboard
from app.models.user import User


router = Router(name="menu_callback")


@router.callback_query(
    F.data.startswith("travels_page"), RegisteredCallback(), StateFilter(None),
)
async def travels_callback(callback: CallbackQuery) -> None:
    page = int(callback.data.replace("travels_page_", ""))

    user = User().get_user_by_telegram_id(callback.from_user.id)

    travels = user.get_user_travels()

    if not travels or travels == []:
        try:
            await callback.message.edit_text(messages.NO_TRAVELS)
        except TelegramBadRequest:
            pass
    else:
        pages = (len(travels) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

        await callback.message.edit_text(
            messages.TRAVELS,
            reply_markup=travels_keyboard(travels, page, pages),
        )
