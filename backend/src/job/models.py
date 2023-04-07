from sqlalchemy import ForeignKey, Column, Integer, Text
from sqlalchemy.orm import relationship
from ..database import Model


class Job(Model):
    __tablename__ = "jobs"

    task_id = Column(Integer, ForeignKey("tasks.id"))
    script = Column(Text, comment="执行脚本")
    state = Column(Integer, default=0, comment="任务状态")

    task = relationship('Task')
