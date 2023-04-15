from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from .schemas import ConnectionSchema, ConnectionCreate
from .curd import search, update, delete
from . import connection_create

router = APIRouter()


class Data(BaseModel):
    code: int
    data: ConnectionSchema


@router.get("", response_model=Page[ConnectionSchema], name="连接列表")
def _search(db: Session = Depends(get_db), user=Depends(session)):
    return search(db)


@router.post("", response_model=Data, name="新建连接")
def _create(item: ConnectionCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = connection_create(db, item)
    return success(data)


@router.patch("/{model_id}", name="更新连接")
def _update(model_id: int, item: ConnectionCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = update(db, model_id, item)
    return success(data)


@router.delete("/{model_id}", name="删除连接")
def _delete(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    data = delete(db, model_id)
    return success(data)
