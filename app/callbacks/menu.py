# type: ignore
__all__ = ()

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app import messages
from app.config import Config
from app.filters.user import RegisteredCallback
from app.keyboards.builders import travels_keyboard
from app.keyboards.profile import get
from app.models.user import User
from app.states.travel import TravelCreationState


router = Router(name="menu_callback")


@router.callback_query(
    F.data == "menu_profile", RegisteredCallback(), StateFilter(None),
)
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
            date_joined=user.get_human_readable_datejoined(),
        ),
        reply_markup=get(),
    )
    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data == "menu_create_travel", RegisteredCallback(), StateFilter(None),
)
async def create_travel_callback(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if callback.data is None or callback.message is None:
        return

    await callback.message.answer(
        messages.CREATE_TRAVEL,
    )
    await callback.message.answer(
        messages.INPUT_TRAVEL_TITLE,
    )
    await state.set_state(TravelCreationState.title)

    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data == "menu_travels", RegisteredCallback(), StateFilter(None),
)
async def travels_callback(
    callback: CallbackQuery,
) -> None:
    page = 0

    user = User().get_user_by_telegram_id(callback.from_user.id)

    travels = user.get_user_travels()

    if not travels or travels == []:
        await callback.message.answer(messages.NO_TRAVELS)
    else:
        pages = (len(travels) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

        await callback.message.answer(
            messages.TRAVELS,
            reply_markup=travels_keyboard(travels, page, pages),
        )

    await callback.message.delete()
    await callback.answer()
