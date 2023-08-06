from telebot.types import ReplyKeyboardMarkup

from app.keyboards.phone_number.button import share_contact_button

share_contact_keyboard = ReplyKeyboardMarkup()

share_contact_keyboard.row(share_contact_button)
