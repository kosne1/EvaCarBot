from telebot.types import InlineKeyboardMarkup

from app.keyboards.role.button import choose_customer_role_button, choose_executor_role_button

role_keyboard = InlineKeyboardMarkup()

role_keyboard.row(choose_customer_role_button)
role_keyboard.row(choose_executor_role_button)
