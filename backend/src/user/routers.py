from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..response import success
from ..pagination import Page
from ..authentication import session
from . import schemas, tasks

router = APIRouter()


@router.get("", response_model=Page[schemas.User], name="用户列表")
def search(db: Session = Depends(get_db), user=Depends(session)):
    return tasks.search(db)


@router.delete("/{model_id}", name="删除用户")
def remove(model_id, db: Session = Depends(get_db), user=Depends(session)):
    data = tasks.delete(db, model_id)
    return success(data)
