from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str = None

    class Config:
        orm_mode = True
