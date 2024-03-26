__all__ = ("router",)

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app import messages, session
from app.config import Config
from app.filters.user import RegisteredCallback
from app.keyboards.builders import notes_keyboard
from app.keyboards.note import get as notes_get
from app.models.travel import Note, Travel
from app.states.travel import (
    CreateNoteState,
)


router = Router(name="menu_callback")


@router.callback_query(
    F.data.startswith("travel_add_note"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_add_note_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    travel_id = int(callback.data.replace("travel_add_note_", ""))

    travel = Travel.get_travel_by_id(travel_id)

    if not travel or travel == []:
        return

    await state.set_state(CreateNoteState.file_id)
    await state.update_data(travel_id=travel_id)
    await callback.message.answer(
        messages.ADD_NOTE,
    )

    await callback.answer()


@router.message(
    CreateNoteState.file_id,
)
async def create_note_file_id(message: Message, state: FSMContext):
    if message.from_user is None:
        return

    if message.text == "/cancel":
        await message.answer(
            messages.ACTION_CANCELED,
        )

        await state.update_data()
        await message.delete()
        await state.clear()

        return

    if message.photo is None and message.document is None:
        return

    if message.photo is not None:
        await state.update_data(
            file_type="photo",
            file_id=message.photo[-1].file_id,
            file_name="photo",
        )

        # await message.answer_photo(message.photo[-1].file_id)

    elif message.document is not None:
        await state.update_data(
            file_type="document",
            file_id=message.document.file_id,
            file_name=message.document.file_name,
        )

        # await message.answer_document(message.document.file_id)

    data = await state.get_data()

    data["author_id"] = message.from_user.id

    session.add(Note(**data))

    session.commit()

    await message.answer(
        messages.NOTE_ADDED.format(file_name=data["file_name"]),
    )

    await state.clear()


@router.callback_query(
    F.data.startswith("travel_notes_page"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_notes_page_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    travel_id, page = map(
        int,
        callback.data.replace("travel_notes_page_", "").split("_"),
    )

    travel = Travel.get_travel_queryset_by_id(travel_id)

    if not travel or travel == []:
        return

    travel = travel.first()

    notes = Travel().get_notes(callback.from_user.id, travel, public=False)

    pages = (len(notes) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

    try:
        await callback.message.edit_text(
            messages.NOTES,
            reply_markup=notes_keyboard(notes, page, pages, travel.id),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_note_detail"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_note_detail_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    note_id = int(callback.data.replace("travel_note_detail_", ""))

    note = Note.get_note_by_id(note_id)

    if not note or note == []:
        return

    try:
        await callback.message.edit_text(
            note.get_note_text(),
            reply_markup=notes_get(travel_id=note.travel.id, note=note),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_notesend"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_notesend_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    note_id = int(callback.data.replace("travel_notesend_", ""))

    note = Note.get_note_by_id(note_id)

    if not note or note == []:
        return

    if note.file_type == "photo":
        await callback.message.answer_photo(
            note.file_id,
            reply_to_message_id=callback.message.message_id,
        )

    elif note.file_type == "document":
        await callback.message.answer_document(
            note.file_id,
            reply_to_message_id=callback.message.message_id,
        )

    await callback.answer()


@router.callback_query(
    F.data.startswith("travel_note_change_privacy"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_note_change_privacy_callback(
    callback: CallbackQuery,
    state: FSMContext,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    note_id = int(callback.data.replace("travel_note_change_privacy_", ""))

    note = Note().get_note_by_id(note_id)

    if not note or note == []:
        return

    if note.public:
        note.public = False
    else:
        note.public = True

    session.commit()

    try:
        await callback.message.edit_text(
            note.get_note_text(),
            reply_markup=notes_get(travel_id=note.travel.id, note=note),
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("travel_notedelete"),
    RegisteredCallback(),
    StateFilter(None),
)
async def travel_notedelete_callback(
    callback: CallbackQuery,
):
    if (
        callback.message is None
        or callback.data is None
        or not isinstance(callback.message, Message)
    ):
        return

    note_id = int(callback.data.replace("travel_notedelete_", ""))

    note = Note().get_note_queryset_by_id(note_id)

    note_first = note.first()
    file_name = note_first.file_name
    travel = note_first.travel

    if not note or note == []:
        return

    note.delete()

    session.commit()

    notes = Travel().get_notes(callback.from_user.id, travel, public=False)

    pages = (len(notes) + Config.PAGE_SIZE - 1) // Config.PAGE_SIZE

    try:
        await callback.message.edit_text(
            messages.NOTES,
            reply_markup=notes_keyboard(notes, 0, pages, travel.id),
        )
    except TelegramBadRequest:
        pass

    await callback.message.answer(
        messages.NOTE_DELETED.format(file_name=file_name),
    )
