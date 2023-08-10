from app.schemas.ButtonInfoSchema import ButtonInfo

make_order_button_info = ButtonInfo(text="Оставить заказ", callback_data="make_order")
search_order_button_info = ButtonInfo(text="Поиск заказа", callback_data="search_order")
send_help_message_button_info = ButtonInfo(text="Написать в поддержку", callback_data="help")
