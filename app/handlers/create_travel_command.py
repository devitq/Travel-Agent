__all__ = ("router",)

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app import messages, session
from app.filters.user import Registered
from app.models.travel import Travel
from app.states.travel import TravelCreationState
from app.utils.states import delete_message_from_state, handle_validation_error


router = Router(name="create_travel_command")


@router.message(Command("create_travel"), Registered(), StateFilter(None))
async def command_create_travel_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.from_user is None:
        return

    await message.answer(
        messages.CREATE_TRAVEL,
    )
    await message.answer(
        messages.INPUT_TRAVEL_TITLE,
    )

    await state.set_state(TravelCreationState.title)


@router.message(TravelCreationState.title, F.text)
async def name_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.text is None:
        return

    title = message.text.strip()

    if title == "/cancel":
        await message.answer(messages.ACTION_CANCELED)
        await message.delete()

        await delete_message_from_state(state, message.chat.id, message.bot)
        await state.clear()

        return

    try:
        validated_title = Travel().validate_title(key="title", value=title)
    except AssertionError as e:
        await handle_validation_error(message, state, e)

        return

    await delete_message_from_state(state, message.chat.id, message.bot)

    await state.update_data(title=validated_title)
    await state.set_state(TravelCreationState.description)

    await message.answer(
        messages.INPUT_TRAVEL_CALLBACK.format(
            key="title",
            value=validated_title,
        ),
    )
    await message.answer(
        messages.INPUT_TRAVEL_DESCRIPTION,
    )


@router.message(TravelCreationState.description, F.text)
async def description_handler(
    message: Message,
    state: FSMContext,
) -> None:
    if message.text is None or message.from_user is None:
        return

    description = message.text.strip()

    if description == "/cancel":
        await message.answer(messages.ACTION_CANCELED)
        await message.delete()

        await delete_message_from_state(state, message.chat.id, message.bot)
        await state.clear()

        return

    if description == "/skip":
        await state.update_data(description=None)

        await message.answer(messages.INPUT_TRAVEL_DESCRIPTION_SKIPPED)
    else:
        try:
            validated_description = Travel().validate_description(
                key="description",
                value=description,
            )
        except AssertionError as e:
            await handle_validation_error(message, state, e)

            return

        await state.update_data(description=validated_description)
        await state.set_state(TravelCreationState.error_message_id)

        await message.answer(
            messages.INPUT_TRAVEL_CALLBACK.format(
                key="description",
                value=validated_description,
            ),
        )

    await delete_message_from_state(state, message.chat.id, message.bot)

    data = await state.get_data()
    await state.clear()

    if "error_message_id" in data:
        del data["error_message_id"]

    data["author_id"] = message.from_user.id

    session.add(Travel(**data))
    session.commit()

    await message.answer(messages.TRAVEL_CREATED.format(title=data["title"]))
