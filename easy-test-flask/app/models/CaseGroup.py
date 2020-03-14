from lin.exception import NotFound
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String


class CaseGroup(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment='分组id')
    name = Column(String(20), nullable=True, unique=True, comment='分组名称 全局唯一不可重复')
    info = Column(String(50), comment='分组描述')

    @classmethod
    def get_all(cls):
        groups = cls.query.filter_by(delete_time=None).all()
        if not groups:
            raise NotFound(msg='暂无分组')
        return groups