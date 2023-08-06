from telebot.types import InlineKeyboardButton

from app.keyboards.send_order.text import send_order_button_info, cancel_order_button_info, next_order_button_info

send_order_button = InlineKeyboardButton(text=send_order_button_info.text,
                                         callback_data=send_order_button_info.callback_data)
cancel_order_button = InlineKeyboardButton(text=cancel_order_button_info.text,
                                           callback_data=cancel_order_button_info.callback_data)
next_order_button = InlineKeyboardButton(text=next_order_button_info.text,
                                         callback_data=next_order_button_info.callback_data)
