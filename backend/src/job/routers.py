from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from . import schemas, tasks

router = APIRouter()


class Data(BaseModel):
    code: int
    data: schemas.Job


@router.get("", response_model=Page[schemas.Job], name="任务列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.post("", response_model=Data, name="新建任务")
def create(item: schemas.JobCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新任务")
def update(model_id: int, item: schemas.JobUpdate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return success(data)
