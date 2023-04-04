from fastapi import APIRouter
from ship.database import engine, model

model.metadata.create_all(bind=engine)  # 建数据表

router = APIRouter()
