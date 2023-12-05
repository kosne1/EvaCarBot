from pydantic import BaseModel

from app.schemas.UserSchema import RoleUserDto


class CreateOrderDto(BaseModel):
    customer: int = None
    model: str = None
    defect: str = None
    from_address: str | object = None
    to_address: str | object = None
    price: int = None
    datetime: str = None
    type: str = None


class OrderAttributesDto(BaseModel):
    customer: RoleUserDto = None
    executor: RoleUserDto = None
    model: str
    defect: str | None = None
    from_address: str
    to_address: str
    price: int
    datetime: str
    status: str
    type: str


class OrderDto(BaseModel):
    id: int
    attributes: OrderAttributesDto


class SearchOrdersDto(BaseModel):
    orders: list[OrderDto]
