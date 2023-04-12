from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from .config import config

# 定时任务
url = config.get_alchemy_url()
jobstores = {'default': SQLAlchemyJobStore(url=url)}
scheduler = AsyncIOScheduler(jobstores=jobstores)
scheduler.start()
