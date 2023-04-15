from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from .models import Connection
from .schemas import ConnectionCreate


def search(db: Session):
    return paginate(db.query(Connection))


def find(db: Session, model_id: int):
    return db.query(Connection).filter(Connection.id == model_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Connection).filter(Connection.name == name).first()


def create(db: Session, item: ConnectionCreate):
    model = Connection(
        name=item.name,
        host=item.host,
        port=item.port,
        username=item.username,
        password=item.password,
        database=item.database,
        direct=item.direct,
        driver=item.driver,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: ConnectionCreate):
    model = db.query(Connection).filter(Connection.id == model_id).one_or_none()
    if model is None:
        return None
    model.direct = item.direct
    model.driver = item.driver
    model.name = item.name
    model.host = item.host
    model.port = item.port
    model.username = item.username
    model.database = item.database
    if item.password:
        model.password = item.password
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id):
    model = db.query(Connection).filter(Connection.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True
