from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import UserCreate
from .curd import search, find_by_username, create, update, delete


def user_create(db: Session, item: UserCreate):
    data = find_by_username(db, item.username)
    if data:
        raise HTTPException(status_code=500, detail="账号已存在")
    return create(db, item)
