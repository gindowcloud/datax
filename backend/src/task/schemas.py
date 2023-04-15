from datetime import datetime
from pydantic import BaseModel
from ..connection.schemas import ConnectionSchema


class TaskBase(BaseModel):
    reader_id: int
    writer_id: int
    name: str
    query: str
    table: str
    column: str
    date: str = None
    incremental: bool = None

    class Config:
        orm_mode = True


class TaskCreate(TaskBase):
    pass


class TaskSchema(TaskBase):
    id: int = None
    state: int = None
    executed_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None

    reader: ConnectionSchema = None
    writer: ConnectionSchema = None
