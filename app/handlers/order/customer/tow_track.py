from telebot.types import CallbackQuery, Message

from app import bot
from app.api.Order import Orders
from app.api.User import Users
from app.helpers import send_wait_message, auto_sending_order
from app.keyboards.end_order import gen_end_order_keyboard
from app.keyboards.send_order import send_order_keyboard
from app.keyboards.send_order.text import send_order_button_info, cancel_order_button_info
from app.keyboards.start.text import order_tow_track_button_info
from app.services import order_storage_service


@bot.callback_query_handler(func=lambda call: order_tow_track_button_info.filter(call.data))
def make_order(call: CallbackQuery):
    order_storage_service.set_state_making_order(chat_id=call.message.chat.id, user_id=call.from_user.id)
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='Укажите марку/модель в текстовом формате')

    def set_order_model(message: Message):
        order_storage_service.set_order_model(chat_id=message.chat.id, user_id=message.from_user.id,
                                              model=message.text)
        bot.send_message(chat_id=call.message.chat.id, text='Опишите неисправность в текстовом формате')

        bot.register_next_step_handler(call.message, set_order_defect_handler)

    bot.register_next_step_handler(call.message, set_order_model)


def set_order_defect_handler(message: Message):
    order_storage_service.set_order_defect(chat_id=message.chat.id, user_id=message.from_user.id,
                                           defect=message.text)
    bot.send_message(chat_id=message.chat.id, text='Отправьте адрес происшествия с помощью геолокации, '
                                                   'встроенной в телеграм')

    bot.register_next_step_handler(message, set_order_from_address_handler)


def set_order_from_address_handler(message: Message):
    if message.location is None:
        bot.send_message(chat_id=message.chat.id,
                         text='Отправьте адрес происшествия с помощью геолокации, '
                              'встроенной в телеграм')
        bot.register_next_step_handler(message, set_order_from_address_handler)
        return
    order_storage_service.set_order_from_address(chat_id=message.chat.id, user_id=message.from_user.id,
                                                 from_address=message.location)
    bot.send_message(chat_id=message.chat.id, text="Отправьте адрес места прибытия с помощью геолокации, "
                                                   "встроенной в телеграм")

    bot.register_next_step_handler(message, set_order_to_address_handler)


def set_order_to_address_handler(message: Message):
    if message.location is None:
        bot.send_message(chat_id=message.chat.id,
                         text='Отправьте адрес  места прибытия с помощью геолокации, '
                              'встроенной в телеграм')
        bot.register_next_step_handler(message, set_order_to_address_handler)
        return
    new_message = send_wait_message(chat_id=message.chat.id)
    order_storage_service.set_order_to_address(chat_id=message.chat.id, user_id=message.from_user.id,
                                               to_address=message.location)
    order = order_storage_service.gen_create_order_dto(chat_id=message.chat.id, telegram_id=message.from_user.id)
    bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                          text=f"<b>Марка/модель</b>: {order.model}\n"
                               f"<b>Неисправность</b>: {order.defect}\n"
                               f"<b>Адрес отправления</b>: {order.from_address}\n"
                               f"<b>Адрес прибытия</b>: {order.to_address}\n"
                               f"<b>Цена</b>: {order.price} руб.\n\n" +
                               f"Отправляя заказ, вы соглашаетесь с условиями оплаты\n\n"
                               f"Отправить заказ?",
                          reply_markup=send_order_keyboard)


@bot.callback_query_handler(func=lambda call: send_order_button_info.filter(call.data) or
                                              cancel_order_button_info.filter(call.data) and
                                              order_storage_service.is_making_order(chat_id=call.message.chat.id,
                                                                                    user_id=call.from_user.id))
def set_order_state(call: CallbackQuery):
    new_message = send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    if call.data == send_order_button_info.callback_data:
        order_dto = order_storage_service.gen_create_order_dto(chat_id=call.message.chat.id,
                                                               telegram_id=call.from_user.id)
        order = Orders().create(order=order_dto)
        order_storage_service.set_state_waiting_for_executor(chat_id=call.message.chat.id,
                                                             user_id=call.from_user.id,
                                                             order_id=order.id)
        bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                              text='Заказ отправлен, ожидайте исполнителя!')
        auto_sending_order(order=order)
    else:
        order_storage_service.cancel_order(chat_id=call.message.chat.id, user_id=call.from_user.id)
        bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                              text='Заказ отменен!')


@bot.callback_query_handler(func=lambda call: str(call.data).find("set_order_executor_") == 0 and
                                              order_storage_service.is_waiting_for_executor(
                                                  chat_id=call.message.chat.id,
                                                  user_id=call.from_user.id))
def change_order_status(call: CallbackQuery):
    executor_id = int(str(call.data).split("set_order_executor_")[1])
    executor = Users().get(id=executor_id)
    customer = Users().get(telegram_id=call.from_user.id)
    order_id = order_storage_service.get_current_waiting_for_executor_order_id(chat_id=call.message.chat.id,
                                                                               user_id=call.from_user.id)
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
