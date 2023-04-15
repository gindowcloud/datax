from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskSchema, TaskCreate
from .curd import create, find_by_name


def task_create(db: Session, item: TaskCreate):
    data = find_by_name(db, item.name)
    if data:
        raise HTTPException(status_code=500, detail="名称已存在")
    return create(db, item)
