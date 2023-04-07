import time
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db, Model, engine
from .response import success
from .authentication import authenticate, session, password, settings
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


class LoginItem(BaseModel):
    username: str
    password: str


class PasswordItem(BaseModel):
    password: str
    newpassword: str


class SettingsItem(BaseModel):
    name: str


class UserData(BaseModel):
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
def login(item: LoginItem, db: Session = Depends(get_db)):
    data = authenticate(db, item.username, item.password)
    return success(data)


@router.post("/logout")
def logout():
    return success()


@router.get("/profile", response_model=UserData)
def profile(user=Depends(session)):
    return success(user)


@router.post("/profile", response_model=UserData)
def profile(item: SettingsItem, db: Session = Depends(get_db), user=Depends(session)):
    data = settings(db, user, item.name)
    return success(data)


@router.post("/password", response_model=UserData)
def profile(item: PasswordItem, db: Session = Depends(get_db), user=Depends(session)):
    data = password(db, user, item.password, item.newpassword)
    return success(data)


@router.post("/setup", response_model=UserData, name="安装程序")
def setup(db: Session = Depends(get_db)):
    item = schemas.UserCreate(username="admin", password="admin")
    data = tasks.find_by_username(db, item.username)
    if not data:
        data = tasks.create(db, item)
    return success(data)
