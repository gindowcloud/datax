from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import engine, model, get_db
from ..pagination import Page
from ..authentication import session
from . import schemas, tasks

model.metadata.create_all(bind=engine)  # 建数据表

router = APIRouter()


@router.get("", response_model=Page[schemas.User], name="用户列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.delete("/{model_id}", name="删除用户")
def remove(model_id, db: Session = Depends(get_db), user=Depends(session)):
    result = tasks.delete(db, model_id)
    return {
        "code": 200,
        "data": result
    }
