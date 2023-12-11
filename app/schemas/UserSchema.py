from pydantic import BaseModel

from app.schemas.RoleSchema import RoleDto


class CreateUserDto(BaseModel):
    telegram_id: int
    username: str
    full_name: str
    phone_number: str
    role: str
    car: list[str] | None = None


class UserDto(BaseModel):
    id: int
    full_name: str
    username: str
    phone_number: str
    telegram_id: int
    role: RoleDto
    blocked: bool
    confirmed: bool
    car: list[str] | None = None


class UserAttributesDto(BaseModel):
    full_name: str
    username: str
    phone_number: str
    telegram_id: int
    blocked: bool
    confirmed: bool
    car: list[str] | None = None


class UserDataDto(BaseModel):
    id: int
    attributes: UserAttributesDto


class RoleUserDto(BaseModel):
    data: list[UserDataDto]
