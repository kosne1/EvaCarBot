from telebot.types import InlineKeyboardButton


def gen_set_order_executor_button_info(user_id: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(text='Да', callback_data=f"set_order_executor_{user_id}")
