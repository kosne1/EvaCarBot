from telebot.types import CallbackQuery

from app import bot
from app.api.Order import Orders
from app.api.User import Users
from app.helpers import send_wait_message, gen_order_text, convert_datetime
from app.keyboards.accept_order import gen_accept_order_keyboard
from app.keyboards.change_order_status import gen_change_order_status_keyboard
from app.keyboards.start.button import search_order_button
from app.services import order_storage_service


@bot.callback_query_handler(func=lambda call: search_order_button.callback_data == call.data)
def search_order(call: CallbackQuery):
    send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id,
                      text='🔍 Поиск подходящих заказов...')
    order_storage_service.set_state_executor_checking_order(chat_id=call.message.chat.id,
                                                            user_id=call.from_user.id)
    # Получаем список подходящих заказов
    order_ids = order_storage_service.get_checked_orders(chat_id=call.message.chat.id,
                                                         user_id=call.from_user.id)
    orders = Orders().get_waiting_for_executor_orders(checked_order_ids=order_ids)
    # Ищем подходящий заказ
    if len(orders) > 0:
        order = orders[0]
    else:
        bot.send_message(chat_id=call.message.chat.id, text='Для вас нет подходящих заказов!')
        return

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Для вас найдено {len(orders)} подходящих заказов!')

    # Запись текущего просмотренного заказа
    order_storage_service.set_state_executor_checking_order(chat_id=call.message.chat.id,
                                                            user_id=call.from_user.id,
                                                            order_id=order.id)
    bot.send_message(chat_id=call.message.chat.id,
                     text=gen_order_text(order) + "\n\n" +
                          "Принять заказ?", reply_markup=gen_accept_order_keyboard(order_id=order.id))


@bot.callback_query_handler(func=lambda call: str(call.data).find("accept_order_") == 0)
def accept_order(call: CallbackQuery):
    new_message = send_wait_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    order_id = int(str(call.data).split("accept_order_")[1])
    order = Orders().get(order_id=order_id)
    if order.attributes.status != "awaiting executor":
        bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                              text=f'Заказ уже принят другим исполнителем')
        return
    customer_telegram_id = order.attributes.customer.data[0].attributes.telegram_id
    executor = Users().get(telegram_id=call.from_user.id)
    datetime = order.attributes.datetime
    # Отправка сообщения закзчику
    bot.send_message(chat_id=customer_telegram_id,
                     text=f"{executor.full_name} откликнулся на ваш заказ "
                          f"от {convert_datetime(datetime)}!\n\n"
                          f"После подтверждения заказа произойдет обмен контактами.\n"
                          f"Подтвердить заказ?",
                     reply_markup=gen_change_order_status_keyboard(user_id=executor.id))
    bot.edit_message_text(chat_id=new_message.chat.id, message_id=new_message.message_id,
                          text=f'Ожидание заказчика...')
