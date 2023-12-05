from telebot.types import InlineKeyboardButton

order_tow_track_button = InlineKeyboardButton(text="Заказать эвакуатор", callback_data="order_tow_track")
order_car_transporter_button = InlineKeyboardButton(text="Заказать автовоз", callback_data="order_car_transporter")

search_order_button = InlineKeyboardButton(text="Поиск заказа", callback_data="search_order")
send_help_message_button = InlineKeyboardButton(text="Написать в поддержку", callback_data="help")
