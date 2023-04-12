from datetime import datetime
from pydantic import BaseModel
from ..task.schemas import Task


class ScheduleBase(BaseModel):
    task_id: int
    name: str
    type: str
    cron: str = None
    date: str = None
    interval: int = None
    period: str = None
    incremental: bool = None
    executed_at: datetime = None

    class Config:
        orm_mode = True


class ScheduleCreate(ScheduleBase):
    pass


class Schedule(ScheduleBase):
    id: int
    task: Task = None
    created_at: datetime = None
    updated_at: datetime = None
