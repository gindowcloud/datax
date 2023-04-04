from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware
from .routers import router
from .config import config


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

    # 核心路由
    app.include_router(router, prefix=config.prefix)

    return app
