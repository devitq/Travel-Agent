__all__ = ("router",)

import datetime

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import sqlalchemy as sa

from app import messages, session
from app.config import Config
from app.filters.user import Registered, RegisteredCallback
from app.keyboards.builders import locations_keyboard, sights_keyboard
from app.keyboards.confirm_location import get as confirm_location_get
from app.keyboards.location import get as location_get
from app.models.travel import Location, Travel
from app.states.travel import (
    CreateLocationState,
)
from app.utils.geo import get_location_by_name
from app.utils.sights import find_trips, get_info_by_xid
from app.utils.states import delete_message_from_state, handle_validation_error
from app.utils.weather import get_current_weather


router = Router(name="location_callback")


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

    await state.update_data(
        date_end=datetime.datetime.strftime(
            validated_date_end,
            "%Y-%m-%d %H:%M:%S",
        ),
    )

    data = await state.get_data()

    overlapping_location = (
        session.query(Location)
        .filter(
            sa.and_(
                Location.travel_id == data["travel_id"],
                Location.date_start < data["date_end"],
                Location.date_end > data["date_start"],
            ),
        )
        .first()
    )
    if overlapping_location:
        await handle_validation_error(
            message,
            state,
            messages.OVERLAPPING_LOCATION,
        )

        return

    await message.answer(
        messages.INPUT_TRAVEL_CALLBACK.format(
            key="end date",
            value=date_end,
        ),
    )

    await delete_message_from_state(state, message.chat.id, message.bot)

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
    F.data.startswith("travel_locations_page"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_locations_page_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    travel_id, page = map(
        int,
        callback.data.replace("travel_locations_page_", "").split("_"),
    )

    travel = Travel.get_travel_by_id(travel_id)

    if not travel or travel == []:
        return

    locations = Travel.get_sorted_locations(travel)

    pages = (len(locations) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

    try:
        await callback.message.edit_text(
            messages.LOCATIONS,
            reply_markup=locations_keyboard(
                locations,
                page,
                pages,
                travel_id,
            ),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_location_detail"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_detail_location_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    location_id = int(callback.data.replace("travel_location_detail_", ""))

    location = Location.get_location_by_id(location_id)

    if not location or location == []:
        return

    try:
        await callback.message.edit_text(
            location.get_location_text(),
            reply_markup=location_get(location.travel.id, location.id),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_locationdelete"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_locations_delete_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    location_id = int(callback.data.replace("travel_locationdelete_", ""))

    location_queryset = Location.get_location_queryset_by_id(location_id)

    if not location_queryset or location_queryset == []:
        return

    travel = location_queryset.first().travel

    location_queryset.delete()

    session.commit()

    locations = Travel.get_sorted_locations(travel)

    pages = (len(locations) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

    try:
        await callback.message.edit_text(
            messages.LOCATIONS,
            reply_markup=locations_keyboard(
                locations,
                0,
                pages,
                travel.id,
            ),
        )
    except TelegramBadRequest:
        pass

    await callback.message.answer(
        messages.LOCATION_DELETED,
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("travel_locationsights"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_locationsights_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    location_id = int(callback.data.replace("travel_locationsights_", ""))

    location = Location.get_location_by_id(location_id)

    if not location or location == []:
        return

    geocode = get_location_by_name(location.location)

    sights = find_trips(geocode[1].raw.get("lat"), geocode[1].raw.get("lon"))

    if sights is None or len(sights) == 0:
        await callback.message.answer(
            messages.NO_SIGHTS_FOUND.format(
                location=location.location,
                distance=Config.NEARBY_SIGHTS_RADIUS,
            ),
        )
    else:
        await callback.message.answer(
            messages.SIGHTS_HEADER
            + messages.SIGHTS_FOOTER.format(
                location=location.location,
                sights_count=len(sights),
                distance=Config.NEARBY_SIGHTS_RADIUS,
            ),
            reply_markup=sights_keyboard(sights[:20]),
        )

    await callback.answer()


@router.callback_query(
    F.data.startswith("travel_sight_detail"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_sight_detail_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    sight_xid = callback.data.replace("travel_sight_detail_", "")

    await get_info_by_xid(callback, sight_xid)

    await callback.answer()


@router.callback_query(
    F.data.startswith("travel_locationweather"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_locationweather_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    location_id = int(callback.data.replace("travel_locationweather_", ""))

    location = Location.get_location_by_id(location_id)

    if not location or location == []:
        return

    geocode = get_location_by_name(location.location)

    weather = get_current_weather(
        geocode[1].raw.get("lat"),
        geocode[1].raw.get("lon"),
    )

    await callback.message.answer(
        messages.LOCATION_WEATHER.format(
            location=location.location,
            weather_main=weather.get("weather")[0].get("main"),
            temp=weather.get("main").get("temp"),
            feels_like=weather.get("main").get("feels_like"),
            temp_min=weather.get("main").get("temp_min"),
            temp_max=weather.get("main").get("temp_max"),
            pressure=weather.get("main").get("pressure"),
            humidity=weather.get("main").get("humidity"),
        ),
        reply_to_message_id=callback.message.message_id,
    )

    await callback.answer()
