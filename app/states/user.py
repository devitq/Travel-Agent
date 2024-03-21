__all__ = ("RegistrationForm", "UserAltering")

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
