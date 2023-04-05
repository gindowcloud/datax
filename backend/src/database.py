from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from .config import config

engine = create_engine(config.get_alchemy_url(), connect_args={"check_same_thread": False})
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Model:
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.now, comment="创建时间")
    updated_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, comment="更新时间")


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
