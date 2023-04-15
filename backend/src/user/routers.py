from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from .schemas import UserSchema, UserCreate
from .curd import search, update, delete
from . import user_create

router = APIRouter()


class Data(BaseModel):
    code: int
    data: UserSchema


@router.get("", response_model=Page[UserSchema], name="用户列表")
def _search(db: Session = Depends(get_db), user=Depends(session)):
    return search(db)


@router.post("", response_model=Data, name="新建用户")
def _create(item: UserCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = user_create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新用户")
def _update(model_id: int, item: UserCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除用户")
def _delete(model_id, db: Session = Depends(get_db), user=Depends(session)):
    data = delete(db, model_id)
    return success(data)
