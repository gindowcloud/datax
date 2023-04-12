from fastapi import APIRouter, Depends, HTTPException
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
    data: schemas.Schedule


@router.get("", response_model=Page[schemas.Schedule], name="任务列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.post("", response_model=Data, name="新建任务")
def create(item: schemas.ScheduleCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.find_by_name(db, item.name)
    if data:
        raise HTTPException(status_code=500, detail="名称已存在")
    data = tasks.create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新任务")
def update(model_id: int, item: schemas.ScheduleCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除任务")
def remove(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.delete(db, model_id)
    return success(data)
