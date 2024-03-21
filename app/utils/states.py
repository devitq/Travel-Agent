__all__ = ("delete_message_from_state", "handle_validation_error")

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def delete_message_from_state(
    state: FSMContext,
    chat_id: int,
    bot: Bot | None,
) -> None:
    if bot is None:
        return

    data = await state.get_data()

    if (
        "previous_message_id" in data
        and data["previous_message_id"] is not None
    ):
        try:
            await bot.delete_message(
                message_id=data["previous_message_id"],
                chat_id=chat_id,
            )
        except TelegramBadRequest:
            pass

        await state.update_data(previous_message_id=None)

    if (
        "input_message_id" in data
        and data["input_message_id"] is not None
        and "successfully" in data
        and data["successfully"]
    ):
        try:
            await bot.delete_message(
                message_id=data["input_message_id"],
                chat_id=chat_id,
            )
        except TelegramBadRequest:
            pass

        await state.update_data(input_message_id=None)


async def handle_validation_error(
    message: Message,
    state: FSMContext,
    e: AssertionError | str,
) -> None:
    await message.delete()
    await delete_message_from_state(
        state,
        message.chat.id,
        message.bot,
    )

    error_message = await message.answer(str(e))
    await state.update_data(
        previous_message_id=error_message.message_id,
    )
