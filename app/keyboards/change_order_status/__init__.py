from telebot.types import InlineKeyboardMarkup

from app.keyboards.change_order_status.button import gen_set_order_executor_button_info


def gen_change_order_status_keyboard(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    keyboard.row(gen_set_order_executor_button_info(user_id=user_id))

    return keyboard
