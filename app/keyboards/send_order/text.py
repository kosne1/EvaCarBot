from app.schemas.ButtonInfoSchema import ButtonInfo

send_order_button_info = ButtonInfo(text="Да", callback_data="send_order")
cancel_order_button_info = ButtonInfo(text="Нет", callback_data="cancel_order")
next_order_button_info = ButtonInfo(text="Следующий заказ", callback_data="next_order")
