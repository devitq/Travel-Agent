__all__ = ("router",)

import datetime

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import messages, session
from app.config import Config
from app.filters.user import Registered, RegisteredCallback
from app.keyboards.builders import travels_keyboard
from app.keyboards.confirm_location import get as confirm_location_get
from app.keyboards.travel import get as travel_get
from app.models.travel import Location, Travel
from app.models.user import User
from app.states.travel import CreateLocationState, TravelAlteringState
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

    await callback.message.edit_text(
        travel.get_travel_text(),
        reply_markup=travel_get(travel_id),
    )


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
            reply_markup=travel_get(travel_id),
        )
    except TelegramBadRequest:
        pass

    await message.answer(
        messages.TRAVEL_UPDATED,
    )

    await state.clear()


@router.callback_query(
    F.data.startswith("travel_add_location"),
    RegisteredCallback(),
    StateFilter(None),
)
async def add_travel_location_callback(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if (
        callback.data is None
        or callback.message is None
        or not isinstance(callback.message, Message)
    ):
        return

    travel_id = int(callback.data.replace("travel_add_location_", ""))

    travel = Travel().get_travel_by_id(travel_id)

    if not travel:
        return

    await state.update_data(travel_id=travel_id)
    await state.set_state(CreateLocationState.temp_location)

    await callback.message.answer(
        messages.CREATE_LOCATION,
    )
    await callback.message.answer(
        messages.ENTER_LOCATION,
    )

    await callback.answer()


@router.message(CreateLocationState.temp_location, F.text, Registered())
async def location_entered(message: Message, state: FSMContext) -> None:
    if (
        message.text is None
        or message.from_user is None
        or message.bot is None
    ):
        return

    location = message.text.strip()

    if location == "/cancel":
        await message.answer(
            messages.ACTION_CANCELED,
        )

        await state.update_data()
        await message.delete()
        await delete_message_from_state(
            state,
            message.chat.id,
            message.bot,
        )
        await state.clear()

        return

    try:
        validated_location = Location().validate_location(
            key="location",
            value=location,
        )
    except AssertionError as e:
        await handle_validation_error(message, state, e)

        return

    await delete_message_from_state(state, message.chat.id, message.bot)

    await state.update_data(
        temp_location=validated_location,
        temp_location_message_id=message.message_id,
    )
    await state.set_state(CreateLocationState.location)

    await message.answer(
        messages.CONFIRM_LOCATION.format(location=validated_location),
        reply_markup=confirm_location_get(),
    )


@router.callback_query(
    F.data.in_(["confirm_location", "cancel_location"]),
    RegisteredCallback(),
    StateFilter(CreateLocationState.location),
)
async def confirm_location(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if (
        not callback.message
        or not isinstance(callback.message, Message)
        or callback.bot is None
    ):
        return

    data = await state.get_data()
    location = data.get("temp_location")

    if callback.data == "confirm_location":
        await delete_message_from_state(
            state,
            callback.from_user.id,
            callback.bot,
        )

        await state.update_data(location=location)
        await state.set_state(CreateLocationState.date_start)

        await callback.message.answer(
            messages.INPUT_TRAVEL_CALLBACK.format(
                key="location",
                value=location,
            ),
        )
        await callback.message.answer(
            messages.ENTER_LOCATION_DATE_START,
        )
    elif callback.data == "cancel_location":
        error_message = await callback.message.answer(
            messages.CONFIRMATION_REEJECTED,
        )

        try:
            await callback.bot.delete_message(
                callback.from_user.id,
                data["temp_location_message_id"],
            )
        except TelegramBadRequest:
            pass

        await state.set_state(CreateLocationState.temp_location)
        await state.update_data(error_message_id=error_message.message_id)

    try:
        await callback.message.delete()
    except TelegramBadRequest:
        pass

    await callback.answer()


@router.message(CreateLocationState.date_start, F.text, Registered())
async def location_date_start_entered(
    message: Message,
    state: FSMContext,
) -> None:
    if (
        message.text is None
        or message.from_user is None
        or message.bot is None
    ):
        return

    date_start = message.text.strip()

    if date_start == "/cancel":
        await message.answer(
            messages.ACTION_CANCELED,
        )

        await state.update_data()
        await message.delete()
        await delete_message_from_state(
            state,
            message.chat.id,
            message.bot,
        )
        await state.clear()

        return

    try:
        validated_date_start = Location().validate_date_end(
            key="date_start",
            value=date_start,
        )
    except AssertionError as e:
        await handle_validation_error(message, state, e)

        return

    await delete_message_from_state(state, message.chat.id, message.bot)

    await state.update_data(
        date_start=datetime.datetime.strftime(
            validated_date_start,
            "%Y-%m-%d %H:%M:%S",
        ),
    )
    await state.set_state(CreateLocationState.date_end)

    await message.answer(
        messages.INPUT_TRAVEL_CALLBACK.format(
            key="start date",
            value=date_start,
        ),
    )
    await message.answer(
        messages.ENTER_LOCATION_DATE_END,
    )


@router.message(CreateLocationState.date_end, F.text, Registered())
async def location_date_end_entered(
    message: Message,
    state: FSMContext,
) -> None:
    if (
        message.text is None
        or message.from_user is None
        or message.bot is None
    ):
        return

    date_end = message.text.strip()

    if date_end == "/cancel":
        await message.answer(
            messages.ACTION_CANCELED,
        )

        await state.update_data()
        await message.delete()
        await delete_message_from_state(
            state,
            message.chat.id,
            message.bot,
        )
        await state.clear()

        return

    try:
        validated_date_end = Location().validate_date_end(
            key="date_end",
            value=date_end,
        )
    except AssertionError as e:
        await handle_validation_error(message, state, e)

        return

    date_start = (await state.get_data()).get("date_start")

    if validated_date_end <= datetime.datetime.strptime(
        str(date_start),
        "%Y-%m-%d %H:%M:%S",
    ).replace(tzinfo=datetime.UTC):
        await handle_validation_error(
            message,
            state,
            messages.INVALID_DATE_END,
        )

        return

    await delete_message_from_state(state, message.chat.id, message.bot)

    await state.update_data(
        date_end=datetime.datetime.strftime(
            validated_date_end,
            "%Y-%m-%d %H:%M:%S",
        ),
    )

    data = await state.get_data()

    if "temp_location" in data:
        del data["temp_location"]

    if "temp_location_message_id" in data:
        del data["temp_location_message_id"]

    if "error_message_id" in data:
        del data["error_message_id"]

    data["date_start"] = datetime.datetime.strptime(
        data["date_start"],
        "%Y-%m-%d %H:%M:%S",
    )

    data["date_end"] = datetime.datetime.strptime(
        data["date_end"],
        "%Y-%m-%d %H:%M:%S",
    )

    session.add(Location(**data))
    session.commit()

    await message.answer(
        messages.LOCATION_ADDED,
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

    travel = Travel.get_travel_queryset_by_id(travel_id)

    travel.delete()

    session.commit()

    await callback.message.answer(messages.DELETED_TRAVEL)

    await callback.message.delete()

    await callback.answer()
