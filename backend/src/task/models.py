from sqlalchemy import ForeignKey, Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from ..database import Model
from ..connection.models import Connection


class Task(Model):
    __tablename__ = "tasks"

    reader_id = Column(Integer, ForeignKey("connections.id"))
    writer_id = Column(Integer, ForeignKey("connections.id"))
    name = Column(String(80), unique=True, comment="任务名称")
    table = Column(String(50), comment="写数据表")
    query = Column(Text, comment="查询语句")
    column = Column(Text, comment="数据字段")
    timer = Column(String(80), comment="定时器")
    state = Column(Integer, default=0, comment="任务状态 0=无结果 1=已完成 2=已报错")
    executed_at = Column(TIMESTAMP, comment="最后执行时间")

    reader = relationship(Connection, foreign_keys=[reader_id])
    writer = relationship(Connection, foreign_keys=[writer_id])

    jobs = relationship("Job", back_populates="task")
