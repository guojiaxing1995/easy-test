from lin.exception import NotFound, ParameterException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String


class CaseGroup(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment='分组id')
    name = Column(String(20), nullable=False, unique=True, comment='分组名称 全局唯一不可重复')
    info = Column(String(50), comment='分组描述')

    @classmethod
    def new_group(cls, form):
        group = CaseGroup.query.filter_by(name=form.name.data, delete_time=None).first()
        if group is not None:
            raise ParameterException(msg='分组已存在')

        group = CaseGroup.create(
            name = form.name.data,
            info = form.info.data,
            commit=True
        )
        return group

    @classmethod
    def get_all(cls):
        groups = cls.query.filter_by(delete_time=None).all()
        if not groups:
            raise NotFound(msg='暂无分组')
        return groups

    @classmethod
    def search_by_keywords(cls, q):
        groups = cls.query.filter(CaseGroup.name.like('%' + q + '%'), CaseGroup.delete_time == None).all()
        if not groups:
            raise NotFound(msg='暂无分组')
        return groups

    @classmethod
    def edit_group(cls, gid, form):
        group = cls.query.filter_by(id=gid, delete_time=None).first_or_404()
        #name 组内唯一 此处判断不允许重复
        group_by_name = CaseGroup.query.filter_by(name=form.name.data, delete_time=None).first()
        if group_by_name == group:
            group.update(
                id=gid,
                info=form.info.data,
                commit=True
            )
        elif group_by_name is not None:
            raise ParameterException(msg='分组已存在')
        else:
            group.update(
                id=gid,
                name=form.name.data,
                info=form.info.data,
                commit=True
            )
        return True

    @classmethod
    def remove_group(cls, gid):
        group = cls.query.filter_by(id=gid, delete_time=None).first_or_404()
        # 删除分组，逻辑删除
        group.delete(commit=True)
        return True