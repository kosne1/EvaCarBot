import json

import requests

from app.api.API import API
from app.schemas.UserSchema import CreateUserDto, UserDto


class Users(API):
    def __init__(self):
        super().__init__()
        self.api_url += '/users'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def create(self, user: CreateUserDto) -> UserDto:
        confirmed: bool = False if user.role == "executor" else True
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps({
            "username": user.username,
            "email": f"{user.username}@strapi.io",
            "password": f"{user.username}-password",
            "full_name": user.full_name,
            "telegram_id": user.telegram_id,
            "phone_number": user.phone_number,
            "role": 3 if user.role == "executor" else 4,
            "confirmed": confirmed
        })).json()

        if response.get('error', None) is not None:
            if response.get('error').get('message') == 'Email already taken':
                return self.get(telegram_id=user.telegram_id)
        else:
            return UserDto.model_validate(response)

    def get(self, id: int = None, telegram_id: int = None) -> UserDto:
        if telegram_id is not None:
            response = requests.get(self.api_url + f"?filters[telegram_id][$eq]={telegram_id}&populate=*",
                                    headers=self.headers).json()
            if len(response) == 1:
                user_json = response[0]
                return UserDto.model_validate(user_json)
        if id is not None:
            response = requests.get(self.api_url + f"/{id}?populate=*", headers=self.headers).json()
            return UserDto.model_validate(response)
