from pydantic import BaseModel

from app.schemas.UserSchema import RoleUserDto


class CreateOrderDto(BaseModel):
    customer: int
    model: str
    defect: str
    from_address: str
    to_address: str
    price: int
    datetime: str


class OrderAttributesDto(BaseModel):
    customer: RoleUserDto = None
    executor: RoleUserDto = None
    model: str
    defect: str
    from_address: str
    to_address: str
    price: int
    datetime: str
    status: str


class OrderDto(BaseModel):
    id: int
    attributes: OrderAttributesDto


class SearchOrdersDto(BaseModel):
    orders: list[OrderDto]
