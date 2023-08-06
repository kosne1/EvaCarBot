from telebot.types import InlineKeyboardButton

from app.keyboards.role.text import choose_customer_role_button_info, choose_executor_role_button_info

choose_customer_role_button = InlineKeyboardButton(text=choose_customer_role_button_info.text,
                                                   callback_data=choose_customer_role_button_info.callback_data)
choose_executor_role_button = InlineKeyboardButton(text=choose_executor_role_button_info.text,
                                                   callback_data=choose_executor_role_button_info.callback_data)
