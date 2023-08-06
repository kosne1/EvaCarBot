from telebot.types import InlineKeyboardButton

from app.keyboards.accept_order.text import accept_order_button_info, next_order_button_info

accept_order_button = InlineKeyboardButton(text=accept_order_button_info.text,
                                           callback_data=accept_order_button_info.callback_data)
next_order_button = InlineKeyboardButton(text=next_order_button_info.text,
                                         callback_data=next_order_button_info.callback_data)
