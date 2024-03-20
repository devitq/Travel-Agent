__all__ = ("ThrottlingMiddleware",)

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache  # type: ignore


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, time_limit: int | float = 2) -> None:
        self.limit = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,  # type: ignore
        data: Dict[str, Any],
    ) -> Any | None:
        if event.chat.id in self.limit:
            return None

        self.limit[event.chat.id] = None

        return await handler(event, data)
