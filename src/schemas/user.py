from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserAuth(UserCreate):
    pass


class UserUpdate(UserCreate):
    pass


class UserInDBBase(UserBase):
    id_user: UUID
    password: str
    created_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass
