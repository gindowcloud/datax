from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from .schemas import ScheduleSchema, ScheduleCreate
from .curd import search, update
from . import schedule_create, schedule_delete

router = APIRouter()


class Data(BaseModel):
    code: int
    data: ScheduleSchema


@router.get("", response_model=Page[ScheduleSchema], name="任务列表")
def _search(db: Session = Depends(get_db), user=Depends(session)):
    return search(db)


@router.post("", response_model=Data, name="新建任务")
def _create(item: ScheduleCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = schedule_create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新任务")
def _update(model_id: int, item: ScheduleCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除任务")
def _remove(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = schedule_delete(db, model_id)
    return success(data)
