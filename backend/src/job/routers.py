from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from .schemas import JobSchema, JobCreate
from .curd import search, update, logs
from . import job_create

router = APIRouter()


class Data(BaseModel):
    code: int
    data: JobSchema


@router.get("", response_model=Page[JobSchema], name="作业列表")
def _search(task_id: int = None, db: Session = Depends(get_db), user=Depends(session)):
    return search(db, task_id)


@router.post("", response_model=Data, name="新建作业")
def _create(item: JobCreate, back: BackgroundTasks, db: Session = Depends(get_db), user=Depends(session)):
    data = job_create(db, item, back)
    return success(data)


@router.patch("/{model_id}", name="更新作业")
def _update(model_id: int, item: JobCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = update(db, model_id, item)
    return success(data)


@router.get("/{model_id}/logs", name="作业日志")
def _logs(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = logs(db, model_id)
    return success(data)
