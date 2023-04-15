from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from .models import Schedule
from .schemas import ScheduleSchema, ScheduleCreate


def search(db: Session):
    return paginate(db.query(Schedule))


def find(db: Session, model_id: int) -> ScheduleSchema:
    return db.query(Schedule).filter(Schedule.id == model_id).first()


def find_by_name(db: Session, name: str) -> ScheduleSchema:
    return db.query(Schedule).filter(Schedule.name == name).first()


def create(db: Session, item: ScheduleCreate) -> ScheduleSchema:
    model = Schedule(
        task_id=item.task_id,
        name=item.name,
        type=item.type,
        cron=item.cron,
        date=item.date,
        interval=item.interval,
        period=item.period,
        incremental=item.incremental,
    )
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


def update(db: Session, model_id, item: ScheduleCreate) -> ScheduleSchema:
    model = db.query(Schedule).filter(Schedule.id == model_id).one_or_none()
    if model is None:
        return None
    model.task_id = item.task_id
    model.name = item.name
    model.type = item.type
    model.cron = item.cron
    model.interval = item.interval
    model.period = item.period
    model.incremental = item.incremental
    db.commit()
    db.refresh(model)
    return model


def delete(db: Session, model_id) -> bool:
    model = db.query(Schedule).filter(Schedule.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    return True
