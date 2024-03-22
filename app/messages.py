# flake8: noqa

MENU = "<b>Menu:</b>"

WELCOME_MESSAGE = "Hello, <b>{name}</b>! Welcome to the ✈️ Travel Agent bot! Let's start our journey by filling out some information about you."
WELCOME_AGAIN_MESSAGE = "Hello, <b>{name}</b>! Welcome back to the ✈️ Travel Agent bot! If you get lost, you can always call the /help command for assistance."

HELP_MESSAGE = "Help message text."

REGISTERED_MESSAGE = "You have successfully registered. Welcome to the ✈️ Travel Agent bot! \nYou can view and edit your profile using the /profile command."

INPUT_USERNAME = "Enter your username (this will be used to interact with other users):\n<i>Allowed characters: a-z, A-Z, 0-9, _</i>\n<i>Length: 5-20 characters</i>"
INPUT_AGE = "Enter your age:\n<i>Range: 13-120</i>"
INPUT_SEX = "Enter your sex:\n<i>Options: Male or Female</i>"
INPUT_BIO = "Enter your bio (enter /skip if you want to skip this step):\n<i>Maximum length: 100 characters</i>"
INPUT_BIO_SKIPPED = "Sure. You can always fill it later."
INPUT_LOCATION = "Enter your location in this format:\n<i>Format: country, city</i>\n<i>Example: Russia, Moscow</i>"
INPUT_CALLBACK = "All right, your <b>{key}</b> is set to: <b>{value}</b>"
VALIDATION_ERROR = "Invalid input. Please try again."
CANCEL_CHANGE = "<i>Enter /cancel to cancel change.</i>"

PROFILE = (
    "<b>Your profile:</b>\n\n"
    "\tUsername: <b>{username}</b>\n"
    "\tAge: <b>{age}</b>\n"
    "\tSex: <b>{sex}</b>\n"
    "\tCountry: <b>{country}</b>\n"
    "\tCity: <b>{city}</b>\n"
    "\tBio: <b>{bio}</b>\n"
    "\tDate joined: <b>{date_joined}</b>\n"
)
NOT_SET = "<i>Not set</i>"
EDIT_USERNAME = "Enter your username:\n<i>Allowed characters: a-z, A-Z, 0-9, _</i>\n<i>Length: 5-20 characters</i>"
EDIT_BIO = "Enter your bio (enter /skip if you want to set it to None):\n<i>Maximum length: 100 characters</i>"
PROFILE_UPDATED = "✅ Profile updated"
CHANGE_CANCELED = "❌ Change canceled"
