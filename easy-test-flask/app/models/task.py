from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Task(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='任务id')
    project_id = Column(Integer, nullable=False, comment='工程id')
    create_user = Column(Integer, nullable=False, comment='执行人id')
    total = Column(Integer, default=0, comment='用例执行总数')
    success = Column(Integer, default=0, comment='成功数')
    fail = Column(Integer, default=0, comment='失败数')

    def __init__(self, project_id, user_id, total):
        super().__init__()
        self.project_id = project_id
        self.create_user = user_id
        self.total = total

    def new_task(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

    def update_result(self, success=None, fail=None):
        if success is not None:
            self.success = success
        if fail is not None:
            self.fail = fail
        db.session.commit()
