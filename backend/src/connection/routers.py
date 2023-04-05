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
    data: schemas.Connection


@router.get("", response_model=Page[schemas.Connection], name="连接列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.post("", response_model=Data, name="新建连接")
def create(item: schemas.ConnectionCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.find_by_name(db, item.name)
    if data:
        raise HTTPException(status_code=500, detail="名称已存在")
    data = tasks.create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新连接")
def update(model_id: int, item: schemas.ConnectionCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除连接")
def remove(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.delete(db, model_id)
    return success(data)
