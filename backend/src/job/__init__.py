import os
import datetime
from sqlalchemy.orm import Session
from . import schemas, tasks
from .schemas import Job
from ..task.tasks import find as find_task
from ..task.schemas import Task


# 任务脚本
def job_script(db: Session, job: Job):
    # 获取任务信息
    task = find_task(db, job.task_id)
    reader = task.reader
    writer = task.writer
    reader_url = "jdbc:" + reader.driver + "://" + \
                 reader.host + ":" + reader.port + "/" + \
                 reader.database+"?useSSL=false"
    writer_url = "jdbc:" + writer.driver + "://" + \
                 writer.host + ":" + writer.port + "/" + \
                 writer.database + "?useSSL=false"
    # 生成脚本文件
    path = "data/task-" + str(job.task_id)
    if not os.path.exists(path):
        os.mkdir(path)
    script = path + "/job-" + str(job.id) + ".json"
    with open("asset/script.json", mode='r') as file:
        content = file.read()
    content = content.replace("{reader_name}", reader.driver + reader.direct)
    content = content.replace("{reader_jdbcUrl}", reader_url)
    content = content.replace("{querySql}", task.query.replace("\n", " "))
    content = content.replace("{reader_username}", reader.username)
    content = content.replace("{reader_password}", reader.password)
    content = content.replace("{writer_name}", writer.driver + writer.direct)
    content = content.replace("{writer_jdbcUrl}", writer_url)
    content = content.replace("{table}", task.table)
    content = content.replace("{writer_username}", writer.username)
    content = content.replace("{writer_password}", writer.password)
    with open(script, mode='w') as file:
        file.write(content)
    # 变更任务状态
    job.state = 1
    db.commit()
    return task


# 任务执行
def job_execute(db: Session, job: Job, task: Task):
    path = "data/task-" + str(job.task_id)
    script = path + "/job-" + str(job.id) + ".json"
    log = path + "/job-" + str(job.id) + ".log"
    os.system(f"python datax/bin/datax.py " + script + " > " + log)
    job.state = 2
    task.executed_at = datetime.datetime.now()
    db.commit()
