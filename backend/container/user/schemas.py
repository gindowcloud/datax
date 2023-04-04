from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str = None

    class Config:
        orm_mode = True
