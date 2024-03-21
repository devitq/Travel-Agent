__all__ = ("RegistrationForm",)

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext


class RegistrationForm(StatesGroup):
    previous_message = State()
    username = State()
    age = State()
    bio = State()
    sex = State()
    location = State()


class UserAltering(StatesGroup):
    successfully = State()
    message_id = State()
    input_message = State()
    previous_message = State()
    column = State()
    value = State()


async def delete_message_from_state(state: FSMContext) -> None:
    data = await state.get_data()

    if "previous_message" in data and data["previous_message"] is not None:
        try:
            await data["previous_message"].delete()
        except TelegramBadRequest:
            pass

        await state.update_data(previous_message=None)

    if (
        "input_message" in data
        and data["input_message"] is not None
        and "successfully" in data
        and data["successfully"]
    ):
        try:
            await data["input_message"].delete()
        except TelegramBadRequest:
            pass

        await state.update_data(info_message=None)
