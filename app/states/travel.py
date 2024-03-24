__all__ = ()

from aiogram.fsm.state import State, StatesGroup


class TravelCreationState(StatesGroup):
    error_message_id = State()
    title = State()
    description = State()


class TravelAlteringState(StatesGroup):
    travel_message_id = State()
    input_message_id = State()
    error_message_id = State()
    successfully = State()
    travel_id = State()
    column = State()
    value = State()


class CreateLocationState(StatesGroup):
    temp_location_message_id = State()
    error_message_id = State()
    travel_id = State()
    location = State()
    temp_location = State()
    location = State()
    date_start = State()
    date_end = State()
