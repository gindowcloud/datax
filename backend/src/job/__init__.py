import os
import datetime
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from .schemas import JobSchema, JobCreate
from ..task.curd import find as find_task
from ..task.schemas import TaskSchema
from ..config import config
from .curd import create


def job_create(db: Session, item: JobCreate, back: BackgroundTasks):
    job = create(db, item)
    task = job_script(db, job)
    back.add_task(job_execute, db, job, task)  # 执行作业
    return job


# 作业脚本
def job_script(db: Session, job: JobSchema):
    # 获取任务信息
    task = find_task(db, job.task_id)
    where = task.date + " > " + str(task.created_at) if job.incremental else ""  # 查询条件
    pre_sql = "" if job.incremental else "truncate table " + task.table  # 预执行语句
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
    content = content.replace("{column}", task.column.replace("\n", " ").replace(", ", '", "'))
    content = content.replace("{writer_username}", writer.username)
    content = content.replace("{writer_password}", writer.password)
    content = content.replace("{where}", where)
    content = content.replace("{preSql}", pre_sql)
    with open(script, mode='w') as file:
        file.write(content)
    # 变更作业状态
    job.state = 1
    db.commit()
    return task


# 执行作业
def job_execute(db: Session, job: JobSchema, task: TaskSchema):
    # 文件位置
    path = "data/task-" + str(job.task_id)
    script = path + "/job-" + str(job.id) + ".json"
    log = path + "/job-" + str(job.id) + ".log"
    # 执行命令
    cmd = config.python + " " + config.datax + " " + script + " > " + log
    os.system(cmd)
    # 获取结果
    with open(log, mode='r') as file:
        content = file.read()
        if content.find("任务总计耗时") == -1:  # 执行不成功
            job.state = 4
            task.state = 2
        else:
            job.state = 2
            task.state = 1
            task.executed_at = datetime.datetime.now()
        db.commit()
