from pydantic import BaseModel
from ..connection.schemas import Connection


class TaskBase(BaseModel):
    reader_id: int
    writer_id: int
    name: str
    table: str
    query: str
    timer: str = None
    state: bool = None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    reader: Connection = None
    writer: Connection = None
    executed_at: int = None
    created_at: int = None
    updated_at: int = None
