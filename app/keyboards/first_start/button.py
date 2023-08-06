from telebot.types import InlineKeyboardButton

from app.keyboards.first_start.text import register_button_info, sign_in_button_info

register_button = InlineKeyboardButton(text=register_button_info.text,
                                       callback_data=register_button_info.callback_data)
sign_in_button = InlineKeyboardButton(text=sign_in_button_info.text,
                                      callback_data=sign_in_button_info.callback_data)
