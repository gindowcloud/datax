from pydantic import BaseModel


class ConnectionBase(BaseModel):
    name: str
    host: str
    port: str
    username: str
    database: str
    direct: str
    driver: str
    state: bool = None

    class Config:
        orm_mode = True


class ConnectionCreate(ConnectionBase):
    password: str = None
    pass


class Connection(ConnectionBase):
    id: int
    created_at: int = None
    updated_at: int = None
