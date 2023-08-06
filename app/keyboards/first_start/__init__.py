from telebot.types import InlineKeyboardMarkup

from app.keyboards.first_start.button import register_button, sign_in_button

first_start_keyboard = InlineKeyboardMarkup()

first_start_keyboard.row(register_button)
first_start_keyboard.row(sign_in_button)
