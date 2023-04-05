from sqlalchemy import Column, Integer, String, TIMESTAMP
from ..database import Model


class User(Model):
    __tablename__ = "users"

    username = Column(String(50), unique=True, nullable=False, comment="用户账号")
    password = Column(String(80), comment="用户密码")
    name = Column(String(80), comment="用户姓名")
    state = Column(Integer, default=1, comment="使用状态")


class AccessToken(Model):
    __tablename__ = "access_tokens"

    user_id = Column(String(20), nullable=False)
    token = Column(String(80), nullable=False)
    abilities = Column(String(80))
    used_at = Column(TIMESTAMP, comment="最后使用时间")
