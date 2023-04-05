from datetime import datetime
from pydantic import BaseModel
from ..connection.schemas import Connection
from ..job.schemas import Job


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
    jobs: list[Job] = []
    executed_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None
