from telebot.types import InlineKeyboardMarkup

from app.keyboards.send_order.button import cancel_order_button, send_order_button

send_order_keyboard = InlineKeyboardMarkup()
send_order_keyboard.row(send_order_button, cancel_order_button)
