from telegram import ReplyKeyboardMarkup, KeyboardButton

def create_register_button():
    keyboard = [[KeyboardButton("ЗАРЕГИСТРИРОВАТЬСЯ")]]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def create_profile_play_buttons():
    keyboard = [
        [KeyboardButton("ПРОФИЛЬ"), KeyboardButton("ИГРАТЬ")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
