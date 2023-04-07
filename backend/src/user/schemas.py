from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str = None
    name: str = None
    state: int = 1

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str = None
    pass


class User(UserBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
