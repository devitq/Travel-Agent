__all__ = ("UserRegistration", "UserAltering")

from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    error_message_id = State()
    username = State()
    age = State()
    bio = State()
    sex = State()
    location = State()


class UserAltering(StatesGroup):
    column = State()
    value = State()
    profile_message_id = State()
    input_message_id = State()
    error_message_id = State()
    successfully = State()
