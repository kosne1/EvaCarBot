from telebot.types import InlineKeyboardMarkup

from app.keyboards.start.button import make_order_button, search_order_button

customer_start_keyboard = InlineKeyboardMarkup()
customer_start_keyboard.row(make_order_button)


executor_start_keyboard = InlineKeyboardMarkup()
executor_start_keyboard.row(search_order_button)
