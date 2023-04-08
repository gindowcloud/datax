from sqlalchemy.orm import Session
from . import schemas, tasks
from .schemas import Job
from ..task.tasks import find


# 运行任务
def run_job(db: Session, model: Job):
    task = find(db, model.task_id)
    reader = task.reader
    writer = task.writer
    reader_url = "jdbc:" + reader.driver + "://" + \
                 reader.host + ":" + reader.port + "/" + \
                 reader.database+"?useSSL=false"
    writer_url = "jdbc:" + writer.driver + "://" + \
                 writer.host + ":" + writer.port + "/" + \
                 writer.database + "?useSSL=false"
    print(task)
    # 生成脚本文件
    with open("data/script.example", mode='r') as file:
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
    with open("data/job-" + str(task.id) + ".json", mode='w') as file:
        file.write(content)
    # 变更任务状态
    model.state = 1
    db.commit()
    pass
