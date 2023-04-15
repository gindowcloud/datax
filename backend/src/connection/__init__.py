from fastapi import HTTPException
from sqlalchemy.orm import Session
from .schemas import ConnectionSchema, ConnectionCreate
from .curd import search, find_by_name, create, update, delete


def connection_create(db: Session, item: ConnectionCreate):
    data = find_by_name(db, item.name)
    if data:
        raise HTTPException(status_code=500, detail="名称已存在")
    return create(db, item)
