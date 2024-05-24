from telegram import ReplyKeyboardMarkup

def create_register_button():
    keyboard = [['ЗАРЕГИСТРИРОВАТЬСЯ']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

def create_profile_play_buttons():
    keyboard = [['ПРОФИЛЬ', 'ИГРАТЬ']]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
