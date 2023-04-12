from sqlalchemy import ForeignKey, Column, Integer, String, TIMESTAMP, Text, Boolean
from sqlalchemy.orm import relationship
from ..database import Model


class Schedule(Model):
    __tablename__ = "schedules"

    task_id = Column(Integer, ForeignKey("tasks.id"))
    name = Column(String(80), unique=True, comment="计划名称")
    type = Column(String(50), comment="计划类型")
    cron = Column(String(50), comment="Cron")
    date = Column(String(50), comment="单次时间")
    interval = Column(Integer, comment="间隔时间")
    period = Column(String(50), comment="间隔同期")
    incremental = Column(Boolean, comment="增量更新")
    executed_at = Column(TIMESTAMP, comment="最后执行时间")

    task = relationship("Task")
