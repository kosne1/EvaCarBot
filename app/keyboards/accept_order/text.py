from app.schemas.ButtonInfoSchema import ButtonInfo

accept_order_button_info = ButtonInfo(text="Откликнуться", callback_data="accept_order")
next_order_button_info = ButtonInfo(text="Следующий заказ", callback_data="next_order")
