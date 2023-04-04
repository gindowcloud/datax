from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from ship.database import model


class User(model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(80))
    name = Column(String(80))
    state = Column(Boolean)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


class AccessToken(model):
    __tablename__ = "access_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    token = Column(String(80), nullable=False)
    abilities = Column(String(80))
    used_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
