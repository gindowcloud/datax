from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from ..database import model


class Task(model):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    reader_id = Column(Integer, ForeignKey("connections.id"))
    writer_id = Column(Integer, ForeignKey("connections.id"))
    name = Column(String(80), unique=True)
    table = Column(String(50))
    query = Column(Text)
    timer = Column(String(80))
    state = Column(Boolean)
    executed_at = Column(TIMESTAMP)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    reader = relationship("Connection", foreign_keys=[reader_id])
    writer = relationship("Connection", foreign_keys=[writer_id])
