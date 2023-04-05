from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from ..database import model


class Connection(model):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)
    host = Column(String(50))
    port = Column(String(50))
    username = Column(String(50))
    password = Column(String(50))
    database = Column(String(50))
    driver = Column(String(50))
    direct = Column(String(50))
    state = Column(Boolean)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)
