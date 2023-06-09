from sqlalchemy import ForeignKey, Column, Integer, String, TIMESTAMP, Text, Boolean
from sqlalchemy.orm import relationship
from ..database import Model


class Task(Model):
    __tablename__ = "tasks"

    reader_id = Column(Integer, ForeignKey("connections.id"))
    writer_id = Column(Integer, ForeignKey("connections.id"))
    name = Column(String(80), unique=True, comment="任务名称")
    query = Column(Text, comment="查询语句")
    date = Column(String(50), comment="日期字段")
    table = Column(String(50), comment="写数据表")
    column = Column(Text, comment="数据字段")
    incremental = Column(Boolean, comment="增量更新")
    state = Column(Integer, default=0, comment="任务状态 0=无结果 1=已完成 2=已报错")
    executed_at = Column(TIMESTAMP, comment="最后执行时间")

    reader = relationship("Connection", foreign_keys=[reader_id])
    writer = relationship("Connection", foreign_keys=[writer_id])

    jobs = relationship("Job", back_populates="task")
