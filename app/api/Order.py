import json

import requests

from app.api.API import API
from app.schemas.OrderSchema import CreateOrderDto, OrderDto


class Orders(API):
    def __init__(self):
        super().__init__()
        self.api_url += '/orders'
        self.headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

    def create(self, order: CreateOrderDto) -> OrderDto:
        response = requests.post(self.api_url, headers=self.headers, data=json.dumps({
            "data": {
                "price": order.price,
                "model": order.model,
                "defect": order.defect,
                "from_address": order.from_address,
                "to_address": order.to_address,
                "datetime": order.datetime,
                "customer": order.customer
            }
        })).json()
        data = response.get("data", None)
        return OrderDto.model_validate(data)

    def update(self, order_id: int, executor: int = None, status: str = None) -> OrderDto:
        data = {}
        if executor is not None and status is not None:
            data = {
                "executor": None if executor == -1 else executor,
                "status": status
            }
        elif executor is not None:
            data = {
                "executor": None if executor == -1 else executor,
            }
        elif status is not None:
            data = {
                "status": status
            }
        data = json.dumps({"data": data})
        response = requests.put(f'{self.api_url}/{order_id}?populate=*', data=data,
                                headers=self.headers).json()
        return OrderDto.model_validate(response.get("data", None))

    def get(self, order_id: int) -> OrderDto:
        response = requests.get(f'{self.api_url}/{order_id}?populate=*',
                                headers=self.headers).json()
        return OrderDto.model_validate(response.get("data", None))

    def get_waiting_for_executor_orders(self, checked_order_ids: list[int] = None) -> list[OrderDto]:
        filters = '?filters[status][$eq]=waiting for executor'
        sort = '&sort=id:desc'
        url = self.api_url + filters + '&populate=*' + sort
        response = requests.get(url, headers=self.headers).json()
        data = response.get("data", None)
        return [OrderDto.model_validate(order) for order in data
                if OrderDto.model_validate(order).id not in checked_order_ids]
