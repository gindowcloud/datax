from datetime import datetime
from pydantic import BaseModel


class JobBase(BaseModel):
    task_id: int = None
    incremental: bool = None
    state: int = None

    class Config:
        orm_mode = True


class JobCreate(JobBase):
    pass


class JobSchema(JobBase):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None
