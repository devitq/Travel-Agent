# flake8: noqa

MENU = "<b>Menu:</b>"

CREATE_LOCATION = "✈️ Lets create new location!"
ENTER_LOCATION = "Enter location:"
CONFIRM_LOCATION = "Is this location correct: <b>{location}</b>?"
CONFIRMATION_REEJECTED = (
    "❌ Confirmation rejected. Please re-enter the location."
)
ENTER_LOCATION_DATE_START = "Enter location start datetime(in UTC) in this format:\n<i>Format: YYYY-MM-DD HH:MM</i>\n<i>Example: 2022-01-01 00:00</i>"
ENTER_LOCATION_DATE_END = "Enter location end datetime(in UTC) in this format:\n<i>Format: YYYY-MM-DD HH:MM</i>\n<i>Example: 2022-01-01 00:00</i>"
INVALID_DATE_END = "End date can't be earlier or equal to start date."
LOCATION_ADDED = "✅ Location added"

DELETED_TRAVEL = "✅ Travel deleted"
TRAVELS = "📃 <b>Travels:</b>\n<i>👑 - owner</i>"
NO_TRAVELS = "No travels yet. You can create one with /create_travel command."
CREATE_TRAVEL = (
    "🧳 Let's create new travel!\n<i>Enter /cancel to cancel creating.</i>"
)
TRAVEL_UPDATED = "✅ Travel updated"
EDIT_TRAVEL_DESCRIPTION = "Enter travel description (enter /skip if you want to set it to None):\n<i>Maximum length: 100 characters</i>"
INPUT_TRAVEL_TITLE = (
    "Enter travel title:\n<i>Maximum length: 30 characters</i>"
)
INPUT_TRAVEL_CALLBACK = (
    "All right, travel <b>{key}</b> is set to: <b>{value}</b>"
)
INPUT_TRAVEL_DESCRIPTION = "Enter travel description (enter /skip if you want to skip this step):\n<i>Maximum length: 100 characters</i>"
INPUT_TRAVEL_DESCRIPTION_SKIPPED = "✅ Sure. You can always fill it later."
TRAVEL_CREATED = "Travel <b>{title}</b> successfully created! You can now view and edit it in the travels list (/travels command)."
ACTION_CANCELED = "❌ Action canceled"
TRAVEL_DETAIL = (
    "📝 <b>Travel detail</b>\n\n"
    "\tID: <b>{travel_id}</b>\n"
    "\tTitle: <b>{title}</b>\n"
    "\tDescription: <b>{description}</b>\n"
)

WELCOME_MESSAGE = "Hello, <b>{name}</b>! Welcome to the ✈️ Travel Agent bot! Let's start our journey by filling out some information about you."
WELCOME_AGAIN_MESSAGE = "Hello, <b>{name}</b>! Welcome back to the ✈️ Travel Agent bot! If you get lost, you can always call the /help command for assistance."

HELP_MESSAGE = (
    "Welcome to the ✈️ Travel Agent bot! Here is list of commands you can use:\n\n"
    "/start - Start the bot\n"
    "/help - Show this message\n"
    "/menu - Show the main menu\n"
    "/profile - View and edit your profile\n"
    "/create_travel - Create new travel\n"
    "/travels - View and edit your travels\n"
    "/cancel - Cancel the current action\n\n"
    "❓ If you have any questions/issues, feel free to contact us via @itq_travel_agent_support_bot on Telegram."
)

REGISTERED_MESSAGE = "You have successfully registered. Welcome to the ✈️ Travel Agent bot! \nYou can view and edit your profile using the /profile command."

INPUT_USERNAME = "Enter your username (this will be used to interact with other users):\n<i>Allowed characters: a-z, A-Z, 0-9, _</i>\n<i>Length: 5-20 characters</i>"
INPUT_AGE = "Enter your age:\n<i>Range: 13-120</i>"
INPUT_SEX = "Enter your sex:\n<i>Options: Male or Female</i>"
INPUT_BIO = "Enter your bio (enter /skip if you want to skip this step):\n<i>Maximum length: 100 characters</i>"
INPUT_BIO_SKIPPED = "✅ Sure. You can always fill it later."
INPUT_LOCATION = "Enter your location in this format:\n<i>Format: country, city</i>\n<i>Example: Russia, Moscow</i>"
INPUT_CALLBACK = "✅ All right, your <b>{key}</b> is set to: <b>{value}</b>"
VALIDATION_ERROR = "❌ Invalid input. Please try again."
CANCEL_CHANGE = "<i>Enter /cancel to cancel change.</i>"

PROFILE = (
    "<b>👤 Your profile:</b>\n\n"
    "\tUsername: <b>{username}</b>\n"
    "\tAge: <b>{age}</b>\n"
    "\tSex: <b>{sex}</b>\n"
    "\tCountry: <b>{country}</b>\n"
    "\tCity: <b>{city}</b>\n"
    "\tBio: <b>{bio}</b>\n"
    "\tDate joined: <b>{date_joined} UTC</b>\n"
)
NOT_SET = "<i>Not set</i>"
EDIT_USERNAME = "Enter your username:\n<i>Allowed characters: a-z, A-Z, 0-9, _</i>\n<i>Length: 5-20 characters</i>"
EDIT_BIO = "Enter your bio (enter /skip if you want to set it to None):\n<i>Maximum length: 100 characters</i>"
PROFILE_UPDATED = "✅ Profile updated"
CHANGE_CANCELED = "❌ Change canceled"

PROCCESSING = "⌛️ Processing..."
