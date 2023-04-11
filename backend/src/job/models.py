from sqlalchemy import ForeignKey, Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from ..database import Model


class Job(Model):
    __tablename__ = "jobs"

    task_id = Column(Integer, ForeignKey("tasks.id"))
    script = Column(Text, comment="执行脚本")
    incremental = Column(Boolean, comment="增量更新")
    state = Column(Integer, default=0, comment="任务状态 0=待处理 1=处理中 2=已完成 3=已取消 4=已报错")

    task = relationship("Task", back_populates="jobs")
