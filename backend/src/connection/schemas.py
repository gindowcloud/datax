from datetime import datetime
from pydantic import BaseModel


class ConnectionBase(BaseModel):
    name: str
    host: str
    port: str
    username: str
    database: str
    direct: str
    driver: str
    state: bool = True

    class Config:
        orm_mode = True


class ConnectionCreate(ConnectionBase):
    password: str = None
    pass


class ConnectionSchema(ConnectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
