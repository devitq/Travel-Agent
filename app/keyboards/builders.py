__all__ = ("sex_keyboard", "travels_keyboard")

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.config import Config


def sex_keyboard(choices: str | list):
    builder = ReplyKeyboardBuilder()

    if isinstance(choices, str):
        choices = [choices]

    [builder.button(text=choice) for choice in choices]
    return builder.as_markup(resize_keyboard=True)


def travels_keyboard(travels: list, page: int, pages: int, user_id: int):
    builder = InlineKeyboardBuilder()
    rows = []

    start_index = page * Config.PAGE_SIZE
    end_index = min((page + 1) * Config.PAGE_SIZE, len(travels))

    for travel in travels[start_index:end_index]:
        button_text = travel.title

        if travel.author_id == user_id:
            button_text += " 👑"

        rows.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"travel_detail_{travel.id}",
            ),
        )

    for _ in range(0, Config.PAGE_SIZE - len(rows)):
        rows.append(InlineKeyboardButton(text=" ", callback_data="pass"))

    builder.row(*rows, width=2)

    navigation_row = []

    if page > 0:
        navigation_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"travels_page_{page - 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    total_pages = 1 if pages == 0 else pages
    navigation_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="pass",
        ),
    )

    if page < pages - 1:
        navigation_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"travels_page_{page + 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    builder.row(*navigation_row)

    return builder.as_markup()


def locations_keyboard(locations: list, page: int, pages: int, travel_id: int):
    builder = InlineKeyboardBuilder()
    rows = []

    start_index = page * Config.PAGE_SIZE
    end_index = min((page + 1) * Config.PAGE_SIZE, len(locations))

    for location in locations[start_index:end_index]:
        button_text = location.location

        rows.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"travel_location_detail_{location.id}",
            ),
        )

    for _ in range(0, Config.PAGE_SIZE - len(rows)):
        rows.append(InlineKeyboardButton(text=" ", callback_data="pass"))

    builder.row(*rows, width=2)

    navigation_row = []

    if page > 0:
        navigation_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"travel_locations_{travel_id}_{page - 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    total_pages = 1 if pages == 0 else pages
    navigation_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="pass",
        ),
    )

    if page < pages - 1:
        navigation_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"travel_locations_{travel_id}_{page + 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    builder.row(*navigation_row)
    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_detail_{travel_id}",
        ),
    )

    return builder.as_markup()


def notes_keyboard(notes, page: int, pages: int, travel_id: int):
    builder = InlineKeyboardBuilder()

    rows = []

    start_index = page * Config.PAGE_SIZE
    end_index = min((page + 1) * Config.PAGE_SIZE, len(notes))

    for note in notes[start_index:end_index]:
        if note.file_type == "photo":
            button_text = f"Photo ID: {note.id}"
        else:
            button_text = note.file_name

        rows.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"travel_note_detail_{note.id}",
            ),
        )

    for _ in range(0, Config.PAGE_SIZE - len(rows)):
        rows.append(InlineKeyboardButton(text=" ", callback_data="pass"))

    builder.row(*rows, width=2)

    navigation_row = []

    if page > 0:
        navigation_row.append(
            InlineKeyboardButton(
                text="⬅️",
                callback_data=f"travel_notes_page_{travel_id}_{page - 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    total_pages = 1 if pages == 0 else pages
    navigation_row.append(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="pass",
        ),
    )

    if page < pages - 1:
        navigation_row.append(
            InlineKeyboardButton(
                text="➡️",
                callback_data=f"travel_notes_page_{travel_id}_{page + 1}",
            ),
        )
    else:
        navigation_row.append(
            InlineKeyboardButton(
                text=" ",
                callback_data="pass",
            ),
        )

    builder.row(*navigation_row)

    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_detail_{travel_id}",
        ),
    )

    return builder.as_markup()


def sights_keyboard(sights: list):
    builder = InlineKeyboardBuilder()

    rows = []

    for sight in sights:
        button_text = sight[0]

        rows.append(
            InlineKeyboardButton(
                text=button_text,
                callback_data=f"travel_sight_detail_{sight[1]}",
            ),
        )

    for _ in range(0, 20 - len(rows)):
        rows.append(InlineKeyboardButton(text=" ", callback_data="pass"))

    builder.row(*rows, width=2)

    return builder.as_markup()
