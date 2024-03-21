__all__ = ("sex_keyboard",)

from aiogram.utils.keyboard import ReplyKeyboardBuilder


def sex_keyboard(text: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(text, str):
        text = [text]

    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True)
