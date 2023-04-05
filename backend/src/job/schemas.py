from datetime import datetime
from pydantic import BaseModel


class JobBase(BaseModel):
    state: int = None

    class Config:
        orm_mode = True


class JobCreate(JobBase):
    task_id: int
    pass


class JobUpdate(JobBase):
    pass


class Job(JobBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
