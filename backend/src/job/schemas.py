from datetime import datetime
from pydantic import BaseModel


class JobBase(BaseModel):
    task_id: int = None
    state: int = None

    class Config:
        orm_mode = True


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class Job(JobBase):
    id: int
    created_at: datetime = None
    updated_at: datetime = None
