from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from .models import Task
from .schemas import TaskSchema, TaskCreate


def search(db: Session):
    return paginate(db.query(Task))


def find(db: Session, model_id: int):
    return db.query(Task).filter(Task.id == model_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Task).filter(Task.name == name).first()


def create(db: Session, item: TaskCreate):
    model = Task(
        reader_id=item.reader_id,
        writer_id=item.writer_id,
        name=item.name,
        query=item.query,
        date=item.date,
        table=item.table,
        column=item.column,
        incremental=item.incremental,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: TaskCreate):
    model = db.query(Task).filter(Task.id == model_id).one_or_none()
    if model is None:
        return None
    model.reader_id = item.reader_id
    model.writer_id = item.writer_id
    model.name = item.name
    model.query = item.query
    model.date = item.date
    model.table = item.table
    model.column = item.column
    model.incremental = item.incremental
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id):
    model = db.query(Task).filter(Task.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True
