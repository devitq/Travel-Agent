__all__ = ("RegistrationForm",)

from aiogram.fsm.state import State, StatesGroup


class RegistrationForm(StatesGroup):
    username = State()
    age = State()
    bio = State()
    sex = State()
    location = State()


class UserAltering(StatesGroup):
    new_value = State()
