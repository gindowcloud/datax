from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from . import models, schemas


def search(db: Session):
    return paginate(db.query(models.Connection))


def find(db: Session, model_id: str):
    return db.query(models.Connection).filter(models.Connection.id == model_id).first()


def find_by_name(db: Session, name: str):
    return db.query(models.Connection).filter(models.Connection.name == name).first()


def create(db: Session, item: schemas.ConnectionCreate):
    try:
        model = models.Connection(
            name=item.name,
            driver=item.driver,
            host=item.host,
            port=item.port,
            username=item.username,
            password=item.password,
            database=item.database,
        )
        db.add(model)
        db.commit()
        db.refresh(model)
        return model
    except:
        return None


def update(db: Session, model_id, item: schemas.ConnectionCreate):
    model = db.query(models.Connection).filter(models.Connection.id == model_id).one_or_none()
    if model is None:
        return None
    model.name = item.name
    model.driver = item.driver
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
    model = db.query(models.Connection).filter(models.Connection.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True
