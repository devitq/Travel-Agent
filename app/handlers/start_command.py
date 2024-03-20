__all__ = ()

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from app import messages, session
from app.keyboards.builders import profile
from app.models.user import User
from app.utils.states import RegistrationForm


router = Router(name="start_command")


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    if User.user_by_telegram_id_exist(
        telegram_id=message.from_user.id,
    ):
        await message.answer(
            messages.WELCOME_AGAIN_MESSAGE.format(
                name=message.from_user.full_name,
            ),
        )
    else:
        await message.answer(
            messages.WELCOME_MESSAGE.format(
                name=message.from_user.full_name,
            ),
        )

        await state.set_state(RegistrationForm.username)
        await message.answer(messages.INPUT_USERNAME)


@router.message(RegistrationForm.username, F.text)
async def username_handler(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    username = message.text.strip()

    try:
        validated_username = User().validate_username(
            key="username",
            value=username,
        )
    except AssertionError as e:
        await message.answer(str(e))
        return

    await state.update_data(username=validated_username)
    await state.set_state(RegistrationForm.age)

    await message.answer(
        messages.INPUT_CALLBACK.format(
            key="username",
            value=validated_username,
        ),
    )
    await message.answer(messages.INPUT_AGE)


@router.message(RegistrationForm.age, F.text)
async def age_handler(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    age = message.text.strip()

    try:
        validated_age = User().validate_age(key="age", value=age)
    except AssertionError as e:
        await message.answer(str(e))
        return

    await state.update_data(age=validated_age)
    await state.set_state(RegistrationForm.sex)

    await message.answer(
        messages.INPUT_CALLBACK.format(key="age", value=validated_age),
    )
    await message.answer(
        messages.INPUT_SEX,
        reply_markup=profile(["Male", "Female"]),
    )


@router.message(RegistrationForm.sex, F.text)
async def sex_handler(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    sex = message.text.strip().lower()

    if sex not in ["male", "female"]:
        await message.answer(messages.VALIDATION_ERROR_MESSAGE)
        return

    await state.update_data(sex=sex)
    await state.set_state(RegistrationForm.bio)

    await message.answer(
        messages.INPUT_CALLBACK.format(key="sex", value=sex),
        reply_markup=ReplyKeyboardRemove(),
    )
    await message.answer(messages.INPUT_BIO)


@router.message(RegistrationForm.bio, F.text)
async def bio_handler(message: Message, state: FSMContext) -> None:
    if message.text is None:
        return

    bio = message.text.strip()

    if bio == "/skip":
        await state.update_data(bio=None)
        await state.set_state(RegistrationForm.location)

        await message.answer(messages.INPUT_BIO_SKIPPED)
        await message.answer(messages.INPUT_LOCATION)
    else:
        try:
            validated_bio = User().validate_bio(key="bio", value=bio)
        except AssertionError as e:
            await message.answer(str(e))
            return

        await state.update_data(bio=validated_bio)
        await state.set_state(RegistrationForm.location)

        await message.answer(
            messages.INPUT_CALLBACK.format(key="bio", value=validated_bio),
        )
        await message.answer(messages.INPUT_LOCATION)


@router.message(RegistrationForm.location, F.text)
async def location_handler(message: Message, state: FSMContext) -> None:
    if message.text is None or message.from_user is None:
        return

    location = message.text.strip().split(", ")

    if len(location) != 2:
        await message.answer(messages.VALIDATION_ERROR_MESSAGE)
        return

    country, city = location

    try:
        validated_country = User().validate_country(
            key="country",
            value=country,
        )
    except AssertionError as e:
        await message.answer(str(e))
        return

    try:
        validated_city = User().validate_city(
            city=city,
            country=validated_country,
        )
    except AssertionError as e:
        await message.answer(str(e))
        return

    await state.update_data(location=[validated_country, validated_city])
    data = await state.get_data()
    await state.clear()

    await message.answer(
        messages.INPUT_CALLBACK.format(
            key="location",
            value=", ".join([validated_country, validated_city]),
        ),
    )

    data["telegram_id"] = message.from_user.id
    data["country"] = data["location"][0]
    data["city"] = data["location"][1]
    del data["location"]
    session.add(User(**data))
    session.commit()

    await message.answer(messages.REGISTERED_MESSAGE)
