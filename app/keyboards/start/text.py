from app.schemas.ButtonInfoSchema import ButtonInfo

order_tow_track_button_info = ButtonInfo(text="Заказать эвакуатор", callback_data="order_tow_track")
search_order_button_info = ButtonInfo(text="Поиск заказа", callback_data="search_order")
send_help_message_button_info = ButtonInfo(text="Написать в поддержку", callback_data="help")
