from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from . import models, schemas


def search(db: Session):
    return paginate(db.query(models.Task))


def find(db: Session, model_id: int):
    return db.query(models.Task).filter(models.Task.id == model_id).first()


def find_by_name(db: Session, name: str):
    return db.query(models.Task).filter(models.Task.name == name).first()


def create(db: Session, item: schemas.TaskCreate):
    model = models.Task(
        reader_id=item.reader_id,
        writer_id=item.writer_id,
        name=item.name,
        table=item.table,
        query=item.query,
        column=item.column,
        timer=item.timer,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: schemas.TaskCreate):
    model = db.query(models.Task).filter(models.Task.id == model_id).one_or_none()
    if model is None:
        return None
    model.reader_id = item.reader_id
    model.writer_id = item.writer_id
    model.name = item.name
    model.table = item.table
    model.query = item.query
    model.column = item.column
    model.timer = item.timer
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id):
    model = db.query(models.Task).filter(models.Task.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True
