from telebot.types import InlineKeyboardButton

from app.keyboards.start.text import order_tow_track_button_info, send_help_message_button_info, \
    order_car_transporter_button_info

order_tow_track_button = InlineKeyboardButton(text=order_tow_track_button_info.text,
                                              callback_data=order_tow_track_button_info.callback_data)
order_car_transporter_button = InlineKeyboardButton(text=order_car_transporter_button_info.text,
                                                    callback_data=order_car_transporter_button_info.callback_data)

# search_order_button = InlineKeyboardButton(text=search_order_button_info.text,
#                                            callback_data=search_order_button_info.callback_data)
send_help_message_button = InlineKeyboardButton(text=send_help_message_button_info.text,
                                                callback_data=send_help_message_button_info.callback_data)
