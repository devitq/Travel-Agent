__all__ = ("RegistrationForm",)

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    previous_message_id = State()
    username = State()
    age = State()
    bio = State()
    sex = State()
    location = State()


class UserAltering(StatesGroup):
    column = State()
    value = State()
    message_id = State()
    input_message_id = State()
    previous_message_id = State()
    successfully = State()


async def delete_message_from_state(
    state: FSMContext,
    chat_id: int,
    bot: Bot | None,
) -> None:
    if bot is None:
        return

    data = await state.get_data()

    if (
        "previous_message_id" in data
        and data["previous_message_id"] is not None
    ):
        try:
            await bot.delete_message(
                message_id=data["previous_message_id"],
                chat_id=chat_id,
            )
        except TelegramBadRequest:
            pass

        await state.update_data(previous_message_id=None)

    if (
        "input_message_id" in data
        and data["input_message_id"] is not None
        and "successfully" in data
        and data["successfully"]
    ):
        try:
            await bot.delete_message(
                message_id=data["input_message_id"],
                chat_id=chat_id,
            )
        except TelegramBadRequest:
            pass

        await state.update_data(input_message_id=None)
