from datetime import datetime

from telebot import StateMemoryStorage

from app.api.User import Users
from app.helpers import get_str_address_by_coords, get_price_by_coords
from app.schemas.OrderSchema import CreateOrderDto


class OrderStorageService:
    def __init__(self):
        self.__storage = StateMemoryStorage()

    def __get_current_state(self, chat_id: int, user_id: int) -> str:
        return str(self.__storage.get_state(chat_id=chat_id, user_id=user_id))

    def set_state_making_order(self, chat_id: int, user_id: int) -> bool:
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='making order')

    def set_order_model(self, chat_id: int, user_id: int, model: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='model', value=model)

    def set_order_defect(self, chat_id: int, user_id: int, defect: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='defect', value=defect)

    def set_order_from_address(self, chat_id: int, user_id: int, from_address: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='from_address', value=from_address)

    def set_order_to_address(self, chat_id: int, user_id: int, to_address: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='to_address', value=to_address)

    def gen_create_order_dto(self, chat_id: int, telegram_id: int) -> CreateOrderDto:
        data = self.__storage.get_data(chat_id=chat_id, user_id=telegram_id)
        user = Users().get(telegram_id=telegram_id)
        return CreateOrderDto(
            customer=user.id,
            model=data.get('model'),
            defect=data.get('defect'),
            from_address=get_str_address_by_coords(data.get('from_address')),
            to_address=get_str_address_by_coords(data.get('to_address')),
            datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            price=get_price_by_coords(data.get('from_address'), data.get('to_address'))
        )

    def cancel_order(self, chat_id: int, user_id: int) -> bool:
        self.__storage.reset_data(chat_id=chat_id, user_id=user_id)
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='authorized')

    def is_making_order(self, chat_id: int, user_id: int) -> bool:
        return self.__get_current_state(chat_id=chat_id, user_id=user_id) == 'making order'

    def set_state_executor_checking_order(self, chat_id: int, user_id: int, order_id: int = None) -> bool:
        self.__storage.set_state(chat_id=chat_id, user_id=user_id, state=f'checking order {order_id}')
        if order_id is not None:
            self.add_watched_orders(chat_id=chat_id, user_id=user_id, order_id=order_id)
        return True

    def set_state_waiting_for_executor(self, chat_id: int, user_id: int, order_id: int) -> bool:
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state=f'waiting for executor {order_id}')

    def is_checking_order(self, chat_id: int, user_id: int) -> bool:
        return self.__get_current_state(chat_id=chat_id, user_id=user_id).find('checking order') == 0

    def get_current_checking_order_id(self, chat_id: int, user_id: int) -> int:
        return int(self.__get_current_state(chat_id=chat_id, user_id=user_id).split('checking order ')[1])

    def add_watched_orders(self, chat_id: int, user_id: int, order_id: int) -> bool:
        order_ids = self.get_checked_orders(chat_id=chat_id, user_id=user_id)
        order_ids.append(order_id)
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id,
                                       key='checked_orders', value=order_ids)

    def get_checked_orders(self, chat_id: int, user_id: int) -> list[int]:
        data = self.__storage.get_data(chat_id=chat_id, user_id=user_id)
        return data.get('checked_orders', [])

    def is_waiting_for_executor(self, chat_id: int, user_id: int) -> bool:
        return self.__get_current_state(chat_id=chat_id, user_id=user_id).find('waiting for executor') == 0

    def get_current_waiting_for_executor_order_id(self, chat_id: int, user_id: int) -> int:
        return int(self.__get_current_state(chat_id=chat_id, user_id=user_id).split('waiting for executor')[1])

    def set_state_authorized(self, chat_id: int, user_id: int) -> bool:
        self.__storage.reset_data(chat_id=chat_id, user_id=user_id)
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='authorized')
