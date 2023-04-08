from fastapi import APIRouter, Depends, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from . import schemas, tasks, job_script, job_execute

router = APIRouter()


class Data(BaseModel):
    code: int
    data: schemas.Job


@router.get("", response_model=Page[schemas.Job], name="任务列表")
def search(task_id: int = None, db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db, task_id)


@router.post("", response_model=Data, name="新建任务")
def create(item: schemas.JobCreate, back: BackgroundTasks, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.create(db, item)
    task = job_script(db, data)
    back.add_task(job_execute, db, data, task)  # 执行任务
    return success(data)


@router.patch("/{model_id}", name="更新任务")
def update(model_id: int, item: schemas.JobUpdate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return success(data)
