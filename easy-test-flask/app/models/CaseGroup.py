from datetime import datetime

from flask import current_app
from flask_jwt_extended import current_user
from lin.db import db
from lin.exception import NotFound, ParameterException, UnknownException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String

from app.libs.enums import UserAuthEnum
from app.libs.error_code import CaseGroupDeleteException
from app.models.UserAuth import UserAuth
from app.models.case import Case


class CaseGroup(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment='分组id')
    name = Column(String(20), nullable=False, unique=True, comment='分组名称 全局唯一不可重复')
    info = Column(String(50), comment='分组描述')

    @classmethod
    def new_group(cls, form):
        group = CaseGroup.query.filter_by(name=form.name.data, delete_time=None).first()
        if group is not None:
            raise ParameterException(msg='分组已存在')
        # 新增分组的时候同时新增可查看当前用例组的人员。当出现问题时进行回滚，人员和分组都不插入
        try:
            group = CaseGroup()
            group.name = form.name.data
            group.info = form.info.data
            db.session.add(group)
            db.session.flush()
            if form.users.data:
                current_app.logger.info(group.id)
                for user in form.users.data:
                    user_auth = UserAuth()
                    user_auth.user_id = user
                    user_auth.auth_id = group.id
                    user_auth.type = UserAuthEnum.GROUP
                    db.session.add(user_auth)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UnknownException(msg='新增异常 数据已回滚')

        return True

    @classmethod
    def get_all(cls):
        groups = cls.query.filter_by(delete_time=None).all()
        if not groups:
            raise NotFound(msg='暂无分组')
        return groups

    @classmethod
    def get_auth(cls):
        '''获取当前用户授权的分组 如果登陆用户是管理员则返回多有用例组'''
        if current_user.id == 1:
            groups = cls.get_all()
        else:
            auths = UserAuth.query.filter_by(user_id=current_user.id, _type=UserAuthEnum.GROUP.value).all()
            gids = [auth.auth_id for auth in auths]
            groups = cls.query.filter(cls.delete_time==None, cls.id.in_(gids)).all()
        if not groups:
            raise NotFound(msg='暂无分组')
        return groups

    @classmethod
    def edit_group(cls, gid, form):
        gid = int(gid)
        group = cls.query.filter_by(id=gid, delete_time=None).first_or_404()
        #name 组内唯一 此处判断不允许重复
        group_by_name = CaseGroup.query.filter_by(name=form.name.data, delete_time=None).first()
        #获取目标分组当前的授权人员
        old_user_auth = UserAuth.query.filter_by(auth_id=gid, _type=UserAuthEnum.GROUP.value).all()
        old_users = [user.user_id for user in old_user_auth]
        #新的授权人员
        new_users = form.users.data
        if group_by_name == group or group_by_name is None:
            try:
                group.id = gid
                group.name = form.name.data
                group.info = form.info.data
                if form.users.data is not None:
                    #旧人员列表中有 新人员列表中没有，这部分删除
                    old = list(set(old_users).difference(set(new_users)))
                    if old:
                        for user_id in old:
                            user = UserAuth.query.filter_by(user_id=user_id, _type=UserAuthEnum.GROUP.value, auth_id=gid).first_or_404()
                            db.session.delete(user)
                    # 新人员列表中有 旧人员列表中没有，这部分新增
                    new = list(set(new_users).difference(set(old_users)))
                    if new:
                        for user_id in new:
                            user_auth = UserAuth()
                            user_auth.user_id = user_id
                            user_auth.auth_id = gid
                            user_auth.type = UserAuthEnum.GROUP
                            db.session.add(user_auth)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise UnknownException(msg='新增异常请检查数据重试')
        elif group_by_name is not None:
            raise ParameterException(msg='分组已存在')

        return True

    @classmethod
    def remove_group(cls, gid):
        group = cls.query.filter_by(id=gid, delete_time=None).first_or_404()
        cases = Case.query.filter_by(case_group=gid, delete_time=None).all()
        if cases:
            raise CaseGroupDeleteException(msg='分组下存在用例无法删除')

        try:
            # 删除分组用户权限表，物理删除
            user_auth = UserAuth.query.filter_by(auth_id=gid, _type=UserAuthEnum.GROUP.value).all()
            if user_auth:
                users = [user.user_id for user in user_auth]
                for user in users:
                    user = UserAuth.query.filter_by(user_id=user, _type=UserAuthEnum.GROUP.value,auth_id=gid).first()
                    db.session.delete(user)
            # 删除分组，逻辑删除
            group.delete_time = datetime.now()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UnknownException(msg='删除异常请重试')
        return True