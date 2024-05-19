__all__ = ("router",)

from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery

router = Router(name="fallback_callback")


@router.callback_query(~StateFilter(None))
async def in_state_callback(callback: CallbackQuery):
    await callback.answer("Fallback text in state", show_alert=True)


@router.callback_query()
async def fallback_callback(callback: CallbackQuery):
    await callback.answer("Fallback text", show_alert=True)
