from datetime import datetime
from pydantic import BaseModel
from ..task.schemas import TaskSchema


class ScheduleBase(BaseModel):
    task_id: int
    name: str
    type: str
    cron: str = None
    date: str = None
    interval: int = None
    period: str = None
    incremental: bool = None

    class Config:
        orm_mode = True


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleSchema(ScheduleBase):
    id: int = None
    executed_at: datetime = None
    created_at: datetime = None
    updated_at: datetime = None

    task: TaskSchema = None

    class Config:
        orm_mode = True
