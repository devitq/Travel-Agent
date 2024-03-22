__all__ = ()

from aiogram.fsm.state import State, StatesGroup


class TravelCreationState(StatesGroup):
    error_message_id = State()
    title = State()
    description = State()
