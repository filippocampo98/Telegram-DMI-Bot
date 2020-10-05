from telegram import KeyboardButton, ReplyKeyboardMarkup


def get_help_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton('❔ Help'),
            KeyboardButton('📫 Segnalazione Rappresentanti'),
            KeyboardButton('📆 Aulario'),
            KeyboardButton('☁️ Cloud')
        ],
    ]
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)
