import time
from datetime import datetime
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from ..scheduler import scheduler
from .models import Schedule
from . import schemas


def func(a1: str = "Hello") -> None:
    print(a1, time.strftime("'%Y-%m-%d %H:%M:%S'"))


def search(db: Session):
    return paginate(db.query(Schedule))


def find(db: Session, model_id: int):
    return db.query(Schedule).filter(Schedule.id == model_id).first()


def find_by_name(db: Session, name: str):
    return db.query(Schedule).filter(Schedule.name == name).first()


def create(db: Session, item: schemas.ScheduleCreate):
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
    # 添加计划
    job_id = str(model.id)
    next_run_time = datetime.fromtimestamp(time.time())  # 开始执行 = 立即开始
    # 定时任务
    if model.type == "cron":
        split = model.cron.split(" ")
        trigger_args = {
            "year": split[0], "month": split[1],
            "week": split[2], "day_of_week": split[3],
            "day": split[4], "hour": split[5],
            "minute": split[6], "second": split[7]
        }
    # 间隔任务
    elif model.type == "interval":
        trigger_args = {model.period: model.interval}
    existed = scheduler.get_job(job_id=job_id)
    if not existed:
        scheduler.add_job(func, model.type, args=([job_id]), id=job_id, next_run_time=next_run_time, **trigger_args)
    return model


def update(db: Session, model_id, item: schemas.ScheduleCreate):
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


def delete(db: Session, model_id):
    model = db.query(Schedule).filter(Schedule.id == model_id).one_or_none()
    if model is None:
        return None
    db.delete(model)
    db.commit()
    # 删除任务
    job = scheduler.get_job(job_id=model.id)
    if job:
        scheduler.remove_job(job.id)
    return True
