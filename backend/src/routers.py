import time
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import get_db
from .authentication import authenticate, session
from .user.schemas import User
from .user.routers import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/users")


class Item(BaseModel):
    username: str
    password: str


class Data(BaseModel):
    code: int
    data: User


# 接口心跳
@router.get("/", name="接口心跳")
async def home():
    return {
        "code": 200,
        "message": "请求成功",
        "data": {
            "status": "up",
            "timestamp": time.time()
        }
    }


@router.post("/login")
async def login(item: Item, db: Session = Depends(get_db)):
    access_token = authenticate(db, item.username, item.password)
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="登陆失败")
    return {
        "code": 200,
        "data": access_token
    }


@router.post("/logout")
async def logout():
    return {
        "code": 200
    }


@router.get("/profile", response_model=Data)
async def profile(user=Depends(session)):
    return {
        "code": 200,
        "data": user
    }
