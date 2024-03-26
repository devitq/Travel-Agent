__all__ = ("router",)

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import messages, session
from app.config import Config
from app.filters.user import Registered, RegisteredCallback
from app.keyboards.builders import travels_keyboard
from app.keyboards.travel import get as travel_get
from app.models.travel import Travel
from app.models.user import User
from app.states.travel import (
    TravelAlteringState,
)
from app.utils.states import delete_message_from_state, handle_validation_error


router = Router(name="menu_callback")


@router.callback_query(
    F.data == "travels",
    RegisteredCallback(),
    StateFilter(None),
)
async def travels_index_callback(callback: CallbackQuery) -> None:
    page = 0

    if callback.from_user is None or not isinstance(callback.message, Message):
        return

    user = User().get_user_by_telegram_id(callback.from_user.id)

    travels = user.get_user_travels()

    if not travels or travels == []:
        try:
            await callback.message.edit_text(messages.NO_TRAVELS)
        except TelegramBadRequest:
            pass
    else:
        pages = (len(travels) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

        try:
            await callback.message.edit_text(
                messages.TRAVELS,
                reply_markup=travels_keyboard(
                    travels,
                    page,
                    pages,
                    user.telegram_id,
                ),
            )
        except TelegramBadRequest:
            pass


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

        try:
            await callback.message.edit_text(
                messages.TRAVELS,
                reply_markup=travels_keyboard(
                    travels,
                    page,
                    pages,
                    user.telegram_id,
                ),
            )
        except TelegramBadRequest:
            pass


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

    try:
        await callback.message.edit_text(
            travel.get_travel_text(),
            reply_markup=travel_get(travel),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_change"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_change_callback(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if (
        callback.data is None
        or callback.message is None
        or not isinstance(callback.message, Message)
    ):
        return

    travel_id, column = callback.data.replace("travel_change_", "").split("_")

    travel = Travel().get_travel_by_id(travel_id)

    if not travel:
        return

    if column == "title":
        message = await callback.message.answer(
            f"{messages.INPUT_TRAVEL_TITLE}\n{messages.CANCEL_CHANGE}",
        )
    elif column == "description":
        message = await callback.message.answer(
            f"{messages.EDIT_TRAVEL_DESCRIPTION}\n{messages.CANCEL_CHANGE}",
        )

    await state.update_data(
        column=column,
        travel_message_id=callback.message.message_id,
        input_message_id=message.message_id,
        travel_id=travel_id,
    )
    await state.set_state(TravelAlteringState.value)

    await callback.answer()


@router.message(TravelAlteringState.value, F.text, Registered())
async def travel_change_entered(message: Message, state: FSMContext) -> None:
    if (
        message.text is None
        or message.from_user is None
        or message.bot is None
    ):
        return

    data = await state.get_data()

    column = data["column"]
    travel_id = data["travel_id"]
    value = message.text.strip()

    if value == "/cancel":
        await message.answer(
            messages.CHANGE_CANCELED,
        )

        await state.update_data(successfully=True)
        await message.delete()
        await delete_message_from_state(
            state,
            message.chat.id,
            message.bot,
        )
        await state.clear()

        return

    if column == "title":
        try:
            validated_title = Travel().validate_title(
                key="title",
                value=value,
            )
        except AssertionError as e:
            await handle_validation_error(message, state, e)

            return

        await state.update_data(value=validated_title, successfully=True)
    elif column == "description":
        if value == "/skip":
            await state.update_data(value=None, successfully=True)
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )
        else:
            try:
                validated_description = Travel().validate_description(
                    key="description",
                    value=value,
                )
            except AssertionError as e:
                await handle_validation_error(message, state, e)

                return

            await state.update_data(
                value=validated_description,
                successfully=True,
            )

    await message.delete()
    await delete_message_from_state(state, message.chat.id, message.bot)

    state_data = await state.get_data()

    travel = Travel().get_travel_queryset_by_id(travel_id)

    data = {state_data["column"]: state_data["value"]}
    travel.update(data)

    session.commit()

    travel = travel.first()
    session.refresh(travel)

    try:
        await message.bot.edit_message_text(
            travel.get_travel_text(),
            message.chat.id,
            state_data["travel_message_id"],
            reply_markup=travel_get(travel),
        )
    except TelegramBadRequest:
        pass

    await message.answer(
        messages.TRAVEL_UPDATED,
    )

    await state.clear()


@router.callback_query(
    F.data.startswith("travel_delete"),
    RegisteredCallback(),
    StateFilter(None),
)
async def delete_travel_callback(
    callback: CallbackQuery,
):
    if callback.data is None or not isinstance(callback.message, Message):
        return

    travel_id = int(callback.data.replace("travel_delete_", ""))

    user = User().get_user_by_telegram_id(callback.from_user.id)

    travel = Travel.get_travel_queryset_by_id(travel_id)

    travel.delete()

    session.commit()

    travels = user.get_user_travels()

    pages = (len(travels) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

    await callback.message.answer(messages.DELETED_TRAVEL)

    await callback.message.edit_text(
        messages.TRAVELS,
        reply_markup=travels_keyboard(
            travels,
            0,
            pages,
            callback.from_user.id,
        ),
    )

    await callback.answer()
