import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db, Model, engine
from .response import success
from .authentication import authenticate, session
from .user import tasks, schemas
from .user.routers import router as user_router
from .task.routers import router as task_router
from .job.routers import router as job_router
from .connection.routers import router as connection_router

Model.metadata.create_all(bind=engine)  # 建数据表

router = APIRouter()
router.include_router(user_router, prefix="/users")
router.include_router(task_router, prefix="/tasks")
router.include_router(job_router, prefix="/jobs")
router.include_router(connection_router, prefix="/connections")


class Item(BaseModel):
    username: str
    password: str


class Data(BaseModel):
    code: int
    data: schemas.User


# 接口心跳
@router.get("/", name="接口心跳")
def home():
    return success({
        "status": "up",
        "timestamp": time.time()
    })


@router.post("/login")
def login(item: Item, db: Session = Depends(get_db)):
    data = authenticate(db, item.username, item.password)
    return success(data)


@router.post("/logout")
def logout():
    return success()


@router.get("/profile", response_model=Data)
def profile(user=Depends(session)):
    return success(user)


@router.post("/init", name="安装程序")
def setup(item: schemas.UserCreate, db: Session = Depends(get_db)):
    item.username = "admin"
    item.password = "admin"
    data = tasks.find_by_username(db, item.username)
    if data:
        raise HTTPException(500, detail="程序已安装")
    data = tasks.create(db, item)
    return success(data)
