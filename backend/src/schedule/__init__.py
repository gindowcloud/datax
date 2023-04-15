import time
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..scheduler import scheduler
from .schemas import ScheduleSchema, ScheduleCreate
from .curd import find_by_name, create, delete


def func(a1: str = "Hello") -> None:
    print(a1, time.strftime("'%Y-%m-%d %H:%M:%S'"))


def schedule_create(db: Session, item: ScheduleCreate):
    # 添加记录
    data = find_by_name(db, item.name)
    if data:
        raise HTTPException(status_code=500, detail="名称已存在")
    schedule = create(db, item)
    # 添加计划
    job_id = str(schedule.id)
    next_run_time = datetime.fromtimestamp(time.time())  # 立即执行
    # 定时任务
    if schedule.type == "cron":
        split = schedule.cron.split(" ")
        trigger_args = {
            "year": split[0], "month": split[1],
            "week": split[2], "day_of_week": split[3],
            "day": split[4], "hour": split[5],
            "minute": split[6], "second": split[7]
        }
    # 间隔任务
    elif schedule.type == "interval":
        trigger_args = {schedule.period: schedule.interval}
    existed = scheduler.get_job(job_id=job_id)
    if not existed:
        scheduler.add_job(func, schedule.type, args=([job_id]), id=job_id, next_run_time=next_run_time, **trigger_args)
    return schedule


def schedule_delete(db: Session, model_id):
    # 删除任务
    job = scheduler.get_job(job_id=model_id)
    if job:
        scheduler.remove_job(job.id)
    # 删除记录
    schedule = delete(db, model_id)
    return schedule
