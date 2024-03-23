__all__ = ("router",)

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app import messages, session
from app.filters.user import Registered, RegisteredCallback
from app.keyboards.builders import sex_keyboard
from app.keyboards.profile import get
from app.models.user import User
from app.states.user import UserAlteringState
from app.utils.states import (
    delete_message_from_state,
    handle_validation_error,
)


router = Router(name="profile_callback")


@router.callback_query(
    F.data.startswith("profile_change_"),
    StateFilter(None),
    RegisteredCallback(),
)
async def profile_change_callback(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    if (
        callback.data is None
        or callback.message is None
        or not isinstance(callback.message, Message)
    ):
        return

    column = callback.data.replace("profile_change_", "")

    if column == "username":
        message = await callback.message.answer(
            f"{messages.EDIT_USERNAME}\n{messages.CANCEL_CHANGE}",
        )
    elif column == "age":
        message = await callback.message.answer(
            f"{messages.INPUT_AGE}\n{messages.CANCEL_CHANGE}",
        )
    elif column == "bio":
        message = await callback.message.answer(
            f"{messages.EDIT_BIO}\n{messages.CANCEL_CHANGE}",
        )
    elif column == "sex":
        message = await callback.message.answer(
            f"{messages.INPUT_SEX}\n{messages.CANCEL_CHANGE}",
            reply_markup=sex_keyboard(["Male", "Female"]),
        )
    elif column == "location":
        message = await callback.message.answer(
            f"{messages.INPUT_LOCATION}\n{messages.CANCEL_CHANGE}",
        )

    await state.update_data(
        column=column,
        profile_message_id=callback.message.message_id,
        input_message_id=message.message_id,
    )
    await state.set_state(UserAlteringState.value)

    await callback.answer()


@router.message(UserAlteringState.value, F.text, Registered())
async def profile_change_entered(message: Message, state: FSMContext) -> None:
    if (
        message.text is None
        or message.from_user is None
        or message.bot is None
    ):
        return

    column = (await state.get_data()).get("column")
    value = message.text.strip()

    if value == "/cancel":
        await message.answer(
            messages.CHANGE_CANCELED,
            reply_markup=ReplyKeyboardRemove(),
        )

        await state.update_data(successfully=True)
        await message.delete()
        await delete_message_from_state(
            state,
            message.chat.id,
            message.bot,
        )
        await state.clear()

        return

    if column == "username":
        try:
            validated_title = User().validate_username(
                key="username",
                value=value,
            )
        except AssertionError as e:
            await handle_validation_error(message, state, e)

            return

        await state.update_data(value=validated_title, successfully=True)
    elif column == "age":
        try:
            validated_age = User().validate_age(key="age", value=value)
        except AssertionError as e:
            await handle_validation_error(message, state, e)

            return

        await state.update_data(value=validated_age, successfully=True)
    elif column == "bio":
        if value == "/skip":
            await state.update_data(value=None, successfully=True)
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )
        else:
            try:
                validated_bio = User().validate_bio(key="bio", value=value)
            except AssertionError as e:
                await handle_validation_error(message, state, e)

                return

            await state.update_data(value=validated_bio, successfully=True)
    elif column == "sex":
        value = value.lower()

        try:
            validated_sex = User().validate_sex(key="sex", value=value)
        except AssertionError as e:
            await handle_validation_error(message, state, e)

            return

        await state.update_data(value=validated_sex, successfully=True)
    elif column == "location":
        location = value.split(", ")

        proccessing_message = await message.answer(messages.PROCCESSING)

        if len(location) != 2:
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )
            await proccessing_message.edit_text(messages.VALIDATION_ERROR)
            await message.delete()

            error_message = proccessing_message
            await state.update_data(
                error_message_id=error_message.message_id,
            )

            return

        country, city = location

        try:
            validated_country = User().validate_country(
                key="country",
                value=country,
            )
        except AssertionError as e:
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )
            await proccessing_message.edit_text("❌ " + str(e))
            await message.delete()

            error_message = proccessing_message
            await state.update_data(
                error_message_id=error_message.message_id,
            )

            return

        try:
            validated_city = User().validate_city(
                city=city,
                country=validated_country,
            )
        except AssertionError as e:
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )
            await proccessing_message.edit_text("❌ " + str(e))
            await message.delete()

            error_message = proccessing_message
            await state.update_data(
                error_message_id=error_message.message_id,
            )

            return

        await delete_message_from_state(state, message.chat.id, message.bot)

        await state.update_data(
            value=[validated_country, validated_city],
            successfully=True,
        )

    await message.delete()
    await delete_message_from_state(state, message.chat.id, message.bot)

    state_data = await state.get_data()

    user = User.get_user_queryset_by_telegram_id(message.from_user.id)

    if isinstance(state_data["value"], list):
        user.update(
            {
                "country": state_data["value"][0],
                "city": state_data["value"][1],
            },
        )

        try:
            await proccessing_message.delete()
        except TelegramBadRequest:
            pass
    else:
        data = {state_data["column"]: state_data["value"]}
        user.update(data)

    session.commit()

    user = user.first()
    session.refresh(user)

    try:
        await message.bot.edit_message_text(
            user.get_profile_text(),
            message.chat.id,
            state_data["profile_message_id"],
            reply_markup=get(),
        )
    except TelegramBadRequest:
        pass

    await message.answer(
        messages.PROFILE_UPDATED,
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()
