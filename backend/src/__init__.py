from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from .routers import router
from .config import config
from .exception import set_exceptions


def create_app():
    
    app = FastAPI()

    # 跨域设置
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 分页功能
    add_pagination(app)

    # 错误返回
    set_exceptions(app)

    # 核心路由
    app.include_router(router, prefix=config.prefix)

    # 定时任务
    url = config.get_alchemy_url()
    jobstores = {'default': SQLAlchemyJobStore(url=url)}
    scheduler = AsyncIOScheduler(jobstores=jobstores)
    scheduler.start()

    return app
