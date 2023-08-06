from pydantic import BaseModel


class RoleDto(BaseModel):
    id: int
    name: str
    type: str
