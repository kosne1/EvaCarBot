from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def gen_end_order_keyboard(order_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton(text="Заказ завершен", callback_data=f"end_order_{order_id}")
    keyboard.row(button)
    button = InlineKeyboardButton(text="Поиск другого исполнителя",
                                  callback_data=f"search_new_executor_for_order_{order_id}")
    keyboard.row(button)
    return keyboard
