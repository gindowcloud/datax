from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from . import schemas
from .models import Job


def search(db: Session, task_id: int = None):
    return paginate(db.query(Job).filter(Job.task_id == task_id).order_by(Job.id.desc()))


def create(db: Session, item: schemas.JobCreate):
    model = Job(
        task_id=item.task_id,
        incremental=item.incremental,
        state=0,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: schemas.JobUpdate):
    model = db.query(Job).filter(Job.id == model_id).one_or_none()
    if model is None:
        return None
    model.incremental = item.incremental
    model.state = item.state
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id):
    model = db.query(Job).filter(Job.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True


def logs(db: Session, model_id):
    model = db.query(Job).filter(Job.id == model_id).one_or_none()
    if model is None:
        return None
    path = "data/task-" + str(model.task_id)
    log = path + "/job-" + str(model.id) + ".log"
    with open(log, mode='r') as file:
        return file.read()
