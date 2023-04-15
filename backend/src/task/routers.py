from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from .schemas import TaskSchema, TaskCreate
from .curd import search, update, delete
from . import task_create


router = APIRouter()


class Data(BaseModel):
    code: int
    data: TaskSchema


@router.get("", response_model=Page[TaskSchema], name="任务列表")
def _search(db: Session = Depends(get_db), user=Depends(session)):
    return search(db)


@router.post("", response_model=Data, name="新建任务")
def _create(item: TaskCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = task_create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新任务")
def _update(model_id: int, item: TaskCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除任务")
def _delete(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = delete(db, model_id)
    return success(data)
