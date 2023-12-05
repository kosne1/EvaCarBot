from telebot.types import InlineKeyboardButton

from app.keyboards.send_order.text import send_order_button_info, cancel_order_button_info, next_order_button_info

send_order_button = InlineKeyboardButton(text="Да", callback_data="send_order")
cancel_order_button = InlineKeyboardButton(text="Нет", callback_data="cancel_order")
next_order_button = InlineKeyboardButton(text="Следующий заказ", callback_data="next_order")
