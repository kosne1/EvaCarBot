from telebot import StateMemoryStorage

from app.schemas.UserSchema import CreateUserDto


class AuthStorageService:
    def __init__(self):
        self.__storage = StateMemoryStorage()

    def set_state_registring(self, chat_id: int, user_id: int) -> bool:
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='registring')

    def set_role(self, chat_id: int, user_id: int, role: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='role', value=role)

    def set_fullname(self, chat_id: int, user_id: int, full_name: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='full_name', value=full_name)

    def set_phone_number(self, chat_id: int, user_id: int, phone_number: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='phone_number', value=phone_number)

    def set_username(self, chat_id: int, user_id: int, username: str) -> bool:
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='username', value=username)

    def is_registring(self, chat_id: int, user_id: int) -> bool:
        return self.__storage.get_state(chat_id=chat_id, user_id=user_id) == 'registring'

    def set_state_registered(self, chat_id: int, user_id: int) -> bool:
        return self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='authorized')

    def get_create_user_dto(self, chat_id: int, telegram_id: int) -> CreateUserDto:
        data = self.__storage.get_data(chat_id=chat_id, user_id=telegram_id)
        return CreateUserDto(telegram_id=telegram_id,
                             username=data.get('username'),
                             full_name=data.get('full_name'),
                             phone_number=data.get('phone_number'),
                             role=data.get('role'))

    def set_user_auth_id(self, chat_id: int, user_id: int, id: int) -> bool:
        self.__storage.set_state(chat_id=chat_id, user_id=user_id, state='authorized')
        self.__storage.reset_data(chat_id=chat_id, user_id=user_id)
        return self.__storage.set_data(chat_id=chat_id, user_id=user_id, key='id', value=id)
