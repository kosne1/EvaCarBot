from telebot.types import CallbackQuery, Message

from app import bot
from app.keyboards.start import order_car_transporter_button


@bot.callback_query_handler(func=lambda call: str(call.data) == order_car_transporter_button.callback_data)
def order_car_transporter(call: CallbackQuery):
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Укажите марку/модель в текстовом формате')

    def set_order_defect_handler(message: Message):
        model = message.text
        bot.send_message(chat_id=message.chat.id, text='Отправьте адрес отправки с помощью геолокации, '
                                                       'встроенной в телеграм')

        # bot.register_next_step_handler(message, set_order_from_address_handler)

    bot.register_next_step_handler(call.message, set_order_defect_handler)

