from app.schemas.ButtonInfoSchema import ButtonInfo

order_tow_track_button_info = ButtonInfo(text="Заказать эвакуатор", callback_data="order_tow_track")
order_car_transporter_button_info = ButtonInfo(text="Заказать автовоз", callback_data="order_car_transporter")
search_order_button_info = ButtonInfo(text="Поиск заказа", callback_data="search_order")
send_help_message_button_info = ButtonInfo(text="Написать в поддержку", callback_data="help")
