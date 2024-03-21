# type: ignore
__all__ = ()

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

from app import messages, session
from app.filters.user_filter import Registered, RegisteredCallback
from app.keyboards.builders import profile
from app.keyboards.profile import get
from app.models.user import User
from app.utils.states import delete_message_from_state, UserAltering


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
    if callback.data is None or callback.message is None:
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
            reply_markup=profile(["Male", "Female"]),
        )
    elif column == "location":
        message = await callback.message.answer(
            f"{messages.INPUT_LOCATION}\n{messages.CANCEL_CHANGE}",
        )

    await state.update_data(
        column=column,
        message_id=callback.message.message_id,
        input_message_id=message.message_id,
    )
    await state.set_state(UserAltering.value)

    await callback.answer()


@router.message(UserAltering.value, F.text, Registered())
async def profile_change_entered(message: Message, state: FSMContext) -> None:
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
            validated_value = User().validate_username(
                key="username",
                value=value,
            )
        except AssertionError as e:
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

            return

        await state.update_data(value=validated_value, successfully=True)
    elif column == "age":
        try:
            validated_age = User().validate_age(key="age", value=value)
        except AssertionError as e:
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

                return

            await state.update_data(value=validated_bio, successfully=True)
    elif column == "sex":
        value = value.lower()

        try:
            validated_sex = User().validate_sex(key="sex", value=value)
        except AssertionError as e:
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

            return

        await state.update_data(value=validated_sex, successfully=True)
    elif column == "location":
        location = value.split(", ")

        if len(location) != 2:
            await message.delete()
            await delete_message_from_state(
                state,
                message.chat.id,
                message.bot,
            )

            error_message = await message.answer(
                messages.VALIDATION_ERROR_MESSAGE,
            )
            await state.update_data(
                previous_message_id=error_message.message_id,
            )

            return

        country, city = location

        try:
            validated_country = User().validate_country(
                key="country",
                value=country,
            )
        except AssertionError as e:
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

            return

        try:
            validated_city = User().validate_city(
                city=city,
                country=validated_country,
            )
        except AssertionError as e:
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

            return

        await delete_message_from_state(state, message.chat.id, message.bot)

        await state.update_data(
            value=[validated_country, validated_city],
            successfully=True,
        )

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
    else:
        data = {state_data["column"]: state_data["value"]}
        user.update(data)

    session.commit()

    user = user.first()
    session.refresh(user)

    try:
        await message.bot.edit_message_text(
            messages.PROFILE.format(
                username=user.username,
                age=user.age,
                bio=user.bio if user.bio else messages.NOT_SET,
                sex=user.sex.capitalize(),
                country=user.country,
                city=user.city,
            ),
            message.chat.id,
            state_data["message_id"],
            reply_markup=get(),
        )
    except TelegramBadRequest:
        pass

    await message.delete()
    await message.answer(
        messages.PROFILE_UPDATED,
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.clear()
