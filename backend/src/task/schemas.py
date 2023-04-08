from datetime import datetime
from pydantic import BaseModel
from ..connection.schemas import Connection


class TaskBase(BaseModel):
    reader_id: int
    writer_id: int
    name: str
    table: str
    query: str
    column: str = None
    timer: str = None
    state: int = None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    reader: Connection = None
    writer: Connection = None
    executed_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
