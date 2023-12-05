import math
from datetime import datetime, timedelta

import geopy as geopy
from geopy.distance import distance
from telebot.types import Message, Location

from app import bot
from app.api.User import Users
from app.configs import env
from app.keyboards.accept_order import gen_accept_order_keyboard
from app.schemas.OrderSchema import OrderDto


def send_wait_message(chat_id: int, message_id: int = None,
                      text: str = 'Пожалуйста, подождите...') -> Message:
    if message_id is None:
        return bot.send_message(chat_id=chat_id, text=text)
    else:
        return bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                     text=text)


# def gen_start_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
#     user = Users().get(telegram_id=telegram_id)
#     if user is None:
#         return first_start_keyboard
#     return executor_start_keyboard if user.role.type == 'executor' else customer_start_keyboard


def get_str_address_by_coords(location: Location) -> str:
    geolocator = geopy.geocoders.Nominatim(user_agent="my_app")
    location = geolocator.reverse(f"{location.latitude}, {location.longitude}")
    return location.address


def get_price_by_coords_and_order_type(location_from: Location, location_to: Location, order_type: string) -> int:
    if order_type == 'car transporter': return 100000
    dist = distance(
        (location_from.latitude, location_from.longitude),
        (location_to.latitude, location_to.longitude)
    ).km
    price = dist * math.pi / 2 * env.RUB_PER_KM + env.ORDER_START_PRICE
    return int(round(price, -1))


def gen_order_text(order: OrderDto) -> str:
    order_info = order.attributes
    defect_string = f"<b>Неисправность</b>: {order_info.defect}\n" if order_info.defect else ""
    return f"Заказ от <b>{convert_datetime(order_info.datetime)}</b>\n" \
           f"<b>Марка/модель</b>: {order_info.model}\n" \
           f"{defect_string}" \
           f"<b>Адрес отправления</b>: {order_info.from_address}\n" \
           f"<b>Адрес прибытия</b>: {order_info.to_address}\n" \
           f"<b>Цена</b>: {order_info.price} руб.\n\n"


def convert_datetime(datetime_str):
    # Convert string to datetime object
    datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Convert datetime object to Moscow time
    datetime_obj = datetime_obj + timedelta(hours=3)

    # Format datetime object as string in desired format
    datetime_str = datetime_obj.strftime('%H:%M %d.%m.%Y')

    return datetime_str


def auto_sending_order(order: OrderDto) -> None:
    text = gen_order_text(order)
    new_order_string = (f"Новый заказ <b>"
                        + ('автовоза' if order.attributes.type == 'car transporter' else 'эвакуатора')
                        + '</b>!\n\n')
    text = new_order_string + text + "\n\n" + "Успейте найти его в ленте, пока на него никто не откликнулся!"
    executors = Users().get_executors()
    for executor in executors:
        if executor.telegram_id == 5504247833:
            bot.send_message(chat_id=executor.telegram_id, text=text,
                             reply_markup=gen_accept_order_keyboard(order_id=order.id))
