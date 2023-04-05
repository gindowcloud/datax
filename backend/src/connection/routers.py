from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import engine, model, get_db
from ..pagination import Page
from ..authentication import session
from . import schemas, tasks

model.metadata.create_all(bind=engine)  # 建数据表

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="名称已存在")
    data = tasks.create(db, item)
    return {
        "code": 200,
        "data": data
    }


@router.patch("/{model_id}", name="更新连接")
def update(model_id: int, item: schemas.ConnectionCreate, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.update(db, model_id, item)
    return {
        "code": 200,
        "data": data
    }


@router.delete("/{model_id}", name="删除连接")
def remove(model_id: int, db: Session = Depends(get_db), user=Depends(session)):
    result = tasks.delete(db, model_id)
    return {
        "code": 200,
        "data": result
    }
