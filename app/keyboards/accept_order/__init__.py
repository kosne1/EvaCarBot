from telebot.types import InlineKeyboardMarkup

from app.keyboards.accept_order.button import accept_order_button, next_order_button
from app.keyboards.start import search_order_button

accept_order_keyboard = InlineKeyboardMarkup()
accept_order_keyboard.row(accept_order_button, search_order_button)
