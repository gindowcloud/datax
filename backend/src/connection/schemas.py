from pydantic import BaseModel


class ConnectionBase(BaseModel):
    name: str
    driver: str
    host: str
    port: str
    username: str
    database: str
    state: bool = None

    class Config:
        orm_mode = True


class ConnectionCreate(ConnectionBase):
    password: str
    pass


class Connection(ConnectionBase):
    id: str
    created_at: int = None
    updated_at: int = None
