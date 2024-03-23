__all__ = ("router",)

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from app import messages
from app.config import Config
from app.filters.user import RegisteredCallback
from app.keyboards.builders import travels_keyboard
from app.keyboards.travel import get
from app.models.travel import Travel
from app.models.user import User


router = Router(name="menu_callback")


@router.callback_query(
    F.data.startswith("travels_page"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travels_callback(callback: CallbackQuery) -> None:
    if callback.data is None or not isinstance(callback.message, Message):
        return

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
            reply_markup=travels_keyboard(
                travels,
                page,
                pages,
                user.telegram_id,
            ),
        )


@router.callback_query(
    F.data.startswith("travel_detail"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_detail_callback(callback: CallbackQuery) -> None:
    if callback.data is None or not isinstance(callback.message, Message):
        return

    travel_id = int(callback.data.replace("travel_detail_", ""))

    travel = Travel().get_travel_by_id(travel_id)

    if not travel:
        return

    await callback.message.edit_text(
        travel.get_travel_text(),
        reply_markup=get(travel_id),
    )
