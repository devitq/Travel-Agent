__all__ = ("UserRegistrationState", "UserAlteringState")

from aiogram.fsm.state import State, StatesGroup


class UserRegistrationState(StatesGroup):
    error_message_id = State()
    username = State()
    age = State()
    bio = State()
    sex = State()
    location = State()


class UserAlteringState(StatesGroup):
    profile_message_id = State()
    input_message_id = State()
    error_message_id = State()
    successfully = State()
    column = State()
    value = State()
