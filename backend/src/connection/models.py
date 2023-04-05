from sqlalchemy import Column, Integer, String
from ..database import Model


class Connection(Model):
    __tablename__ = "connections"

    name = Column(String(80), unique=True, comment="连接名称")
    host = Column(String(50), comment="连接地址")
    port = Column(String(50), comment="连接端口")
    username = Column(String(50), comment="连接用户")
    password = Column(String(50), comment="连接密码")
    database = Column(String(50), comment="数据库名")
    driver = Column(String(50), comment="连接驱动")
    direct = Column(String(50), comment="连接方向")
    state = Column(Integer, default=1, comment="使用状态")
