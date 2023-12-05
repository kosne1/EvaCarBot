from datetime import datetime

from telebot.types import CallbackQuery, Message

from app import bot
from app.api.Order import Orders
from app.api.User import Users
from app.helpers import send_wait_message, auto_sending_order, get_str_address_by_coords, \
    get_price_by_coords_and_order_type
from app.keyboards.end_order import gen_end_order_keyboard
from app.keyboards.send_order import send_order_keyboard, send_order_button, cancel_order_button
from app.keyboards.send_order.text import send_order_button_info
from app.keyboards.start import order_tow_track_button, order_car_transporter_button
from app.schemas.OrderSchema import CreateOrderDto


@bot.callback_query_handler(func=lambda call: call.data in [order_tow_track_button.callback_data,
                                                            order_car_transporter_button.callback_data])
def make_order(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Укажите марку/модель в текстовом формате')
    order_type = 'car transporter' if order_car_transporter_button.callback_data == call.data else 'tow truck'
    user = Users().get(telegram_id=call.from_user.id)
    order = CreateOrderDto(type=order_type, customer=user.id)
    bot.register_next_step_handler(call.message,
                                   set_car_model
                                   if call.data == order_tow_track_button.callback_data
                                   else set_car_defect,
                                   order)


def set_car_model(message: Message, order: CreateOrderDto):
    bot.send_message(chat_id=message.chat.id, text='Опишите неисправность в текстовом формате')
    order.model = message.text
    bot.register_next_step_handler(message, set_car_defect, order)


def set_car_defect(message: Message, order: CreateOrderDto):
    bot.send_message(chat_id=message.chat.id, text='Отправьте адрес происшествия с помощью геолокации, '
                                                   'встроенной в телеграм')
    if order.type == 'tow truck':
        order.defect = message.text
    else:
        order.model = message.text

    bot.register_next_step_handler(message, set_order_from_address_handler, order)


def set_order_from_address_handler(message: Message, order: CreateOrderDto):
    if message.location is None:
        bot.send_message(chat_id=message.chat.id,
                         text='Отправьте адрес происшествия с помощью геолокации, '
                              'встроенной в телеграм')
        bot.register_next_step_handler(message, set_order_from_address_handler, order)
        return
    order.from_address = message.location
    bot.send_message(chat_id=message.chat.id, text="Отправьте адрес места прибытия с помощью геолокации, "
                                                   "встроенной в телеграм")

    bot.register_next_step_handler(message, set_order_to_address_handler, order)


def set_order_to_address_handler(message: Message, order: CreateOrderDto):
    if message.location is None:
        bot.send_message(chat_id=message.chat.id,
                         text='Отправьте адрес  места прибытия с помощью геолокации, '
                              'встроенной в телеграм')
        bot.register_next_step_handler(message, set_order_to_address_handler, order)
        return
    new_message = send_wait_message(chat_id=message.chat.id)
    order.to_address = message.location
    order.price = get_price_by_coords_and_order_type(
        order.__dict__.get("from_address"),
        order.__dict__.get("to_address"),
        order.type)
    order.from_address = get_str_address_by_coords(order.__dict__.get("from_address"))
    order.to_address = get_str_address_by_coords(order.__dict__.get("to_address"))
    order.datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    defect_string = f"<b>Неисправность</b>: {order.defect}\n" if order.defect else ""
    bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                          text=f"<b>Марка/модель</b>: {order.model}\n"
                               f"{defect_string}"
                               f"<b>Адрес отправления</b>: {order.from_address}\n"
                               f"<b>Адрес прибытия</b>: {order.to_address}\n"
                               f"<b>Цена</b>: {order.price} руб.\n\n" +
                               f"Отправляя заказ, вы соглашаетесь с условиями оплаты\n\n"
                               f"Отправить заказ?",
                          reply_markup=send_order_keyboard)
    Orders().create(order=order)


@bot.callback_query_handler(func=lambda call: call.data in [send_order_button.callback_data,
                                                            cancel_order_button.callback_data])
def set_order_state(call: CallbackQuery):
    new_message = send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == send_order_button_info.callback_data:
        order = Orders().get_latest_customer_order(call.from_user.id)
        Orders().update(order_id=order.id, status='awaiting executor')
        bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                              text='Заказ отправлен, ожидайте исполнителя!')
        auto_sending_order(order=order)
    else:
        bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                              text='Заказ отменен!')


@bot.callback_query_handler(func=lambda call: str(call.data).find("set_order_executor_") == 0)
def change_order_status(call: CallbackQuery):
    executor_id = int(str(call.data).split("set_order_executor_")[1])
    executor = Users().get(id=executor_id)
    customer = Users().get(telegram_id=call.from_user.id)
    order_id = Orders().get_latest_customer_order(call.from_user.id, status='awaiting executor').id
    Orders().update(order_id=order_id, executor=executor.id, status="in work")
    # Отправка контакта заказчика исполнителю
    bot.send_message(chat_id=executor.telegram_id,
                     text=f'Вас выбрали в качестве исполнителя!\n\n'
                          f'Контакты заказчика: ')
    bot.send_contact(chat_id=executor.telegram_id, phone_number=customer.phone_number,
                     first_name=customer.full_name)
    # Отправка контакта исполнителя заказчику
    bot.send_message(chat_id=customer.telegram_id,
                     text=f'Исполнитель утвержден!\n\n'
                          f'Контакты исполнителя: ')
    bot.send_contact(chat_id=customer.telegram_id, phone_number=executor.phone_number,
                     first_name=executor.full_name)

    bot.send_message(chat_id=call.message.chat.id, text='Подтвердите завершение заказа.\n'
                                                        'Вы можете начать поиск другого исполнителя, '
                                                        'если возникли проблемы с утвержденным',
                     reply_markup=gen_end_order_keyboard(order_id=order_id))


@bot.callback_query_handler(func=lambda call: str(call.data).find('end_order_') == 0)
def end_order_handler(call: CallbackQuery):
    order_id = int(str(call.data).split('end_order_')[1])
    Orders().update(order_id=order_id, status="completed")
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Заказ завершен!')


@bot.callback_query_handler(func=lambda call: str(call.data).find('search_new_executor_for_') == 0)
def search_new_executor_for_order_handler(call: CallbackQuery):
    new_message = send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    order_id = int(str(call.data).split('search_new_executor_for_order_')[1])
    order = Orders().get(order_id=order_id)
    Orders().update(order_id=order_id, status="waiting for executor", executor=-1)
    bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                          text='Заказ отправлен, ожидайте исполнителя!')
    auto_sending_order(order=order)
