from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.keyboards.accept_order.button import accept_order_button


def gen_accept_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Принять заказ", callback_data=f"accept_order_{order_id}")
    keyboard.add(button)
    return keyboard
