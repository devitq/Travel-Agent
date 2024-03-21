__all__ = ("Unregistered", "Registered", "RegisteredCallback")

from aiogram.filters import Filter
from aiogram.types import CallbackQuery, Message

from app.models.user import User


class Unregistered(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user is None:
            return False

        return not User.user_by_telegram_id_exist(message.from_user.id)


class Registered(Filter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user is None:
            return False

        return User.user_by_telegram_id_exist(message.from_user.id)


class RegisteredCallback(Filter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        return User.user_by_telegram_id_exist(callback.from_user.id)
