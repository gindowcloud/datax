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
    data: schemas.User


@router.get("", response_model=Page[schemas.User], name="用户列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.post("", response_model=Data, name="新建用户")
def create(item: schemas.UserCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.find_by_username(db, item.username)
    if data:
        raise HTTPException(500, detail="账号已存在")
    data = tasks.create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新用户")
def update(model_id: int, item: schemas.UserCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除用户")
def remove(model_id, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.delete(db, model_id)
    return success(data)
