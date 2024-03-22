__all__ = ("sex_keyboard",)

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.config import Config


def sex_keyboard(choices: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(choices, str):
        text = [choices]

    [builder.button(text=txt) for txt in text]
    return builder.as_markup(resize_keyboard=True)


def travels_keyboard(travels: list, page: int, pages: int):
    builder = InlineKeyboardBuilder()
    rows = []

    start_index = page * Config.PAGE_SIZE
    end_index = min((page + 1) * Config.PAGE_SIZE, len(travels))

    for travel in travels[start_index:end_index]:
        rows.append(
            InlineKeyboardButton(
                text=travel.title,
                callback_data=f"travel_detail_{travel.id}",
            ),
        )

    for _ in range(0, Config.PAGE_SIZE - len(rows)):
        rows.append(InlineKeyboardButton(text=" ", callback_data="pass"))

    builder.row(*rows, width=2)

    if pages > 1:
        navigation_row = []

        if page > 0:
            navigation_row.append(
                InlineKeyboardButton(
                    text="⬅️", callback_data=f"travels_page_{page - 1}",
                ),
            )
        else:
            navigation_row.append(
                InlineKeyboardButton(
                    text=" ", callback_data="pass",
                ),
            )

        navigation_row.append(
            InlineKeyboardButton(
                text=f"{page + 1}/{pages}", callback_data="pass",
            ),
        )

        if page < pages - 1:
            navigation_row.append(
                InlineKeyboardButton(
                    text="➡️", callback_data=f"travels_page_{page + 1}",
                ),
            )
        else:
            navigation_row.append(
                InlineKeyboardButton(
                    text=" ", callback_data="pass",
                ),
            )

        builder.row(*navigation_row)

    return builder.as_markup()
