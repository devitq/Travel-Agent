__all__ = ("get",)

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get(travel_id: int, note):
    builder = InlineKeyboardBuilder()

    builder.row(
        types.InlineKeyboardButton(
            text="⏩ View note",
            callback_data=f"travel_notesend_{note.id}",
        ),
    )

    if note.public:
        builder.row(
            types.InlineKeyboardButton(
                text="🔒 Make private",
                callback_data=f"travel_note_change_privacy_{note.id}",
            ),
        )
    else:
        builder.row(
            types.InlineKeyboardButton(
                text="🔓 Make public",
                callback_data=f"travel_note_change_privacy_{note.id}",
            ),
        )

    builder.row(
        types.InlineKeyboardButton(
            text="❌ Delete note",
            callback_data=f"travel_notedelete_{note.id}",
        ),
    )

    builder.row(
        types.InlineKeyboardButton(
            text="⬅️",
            callback_data=f"travel_notes_page_{travel_id}_0",
        ),
    )

    return builder.as_markup()
