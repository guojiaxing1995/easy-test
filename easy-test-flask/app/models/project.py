from datetime import datetime

import requests
from flask import current_app
from flask_jwt_extended import current_user, get_current_user
from lin.db import db
from lin.exception import NotFound, ParameterException, UnknownException, Forbidden
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, text

from app.libs.enums import UserAuthEnum, ProjectTypeEnum
from app.libs.error_code import ProjectConfigException
from app.libs.init import socket_io
from app.models.ConfigCopy import ConfigCopy
from app.models.ConfigRelation import ConfigRelation
from app.models.UserAuth import UserAuth


class Project(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='工程id')
    name = Column(String(20), nullable=False, comment='工程名称 全局唯一不可重复')
    server = Column(String(60), nullable=False, comment='服务地址')
    header = Column(String(500), comment='公共请求头')
    info = Column(String(50), comment='工程描述')
    _type = Column('type', SmallInteger, nullable=False, comment='工程类型 ;  1 -> 关联用例 |  2 -> 用例副本')
    running = Column(Boolean, nullable=False, comment='是否在运行中')
    progress = Column(Integer, default=0, comment='运行进度')
    user_id = Column(Integer, nullable=False, comment='维护人')

    @property
    def type(self):
        return ProjectTypeEnum(self._type).value

    @type.setter
    def type(self, typeEnum):
        self._type = typeEnum.value

    @classmethod
    def new_project(cls, form):
        project = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        if project is not None:
            raise ParameterException(msg='工程已存在')
        # 新增分组的时候同时新增可查看当前用例组的人员。当出现问题时进行回滚，人员和分组都不插入
        try:
            project = Project()
            project.name = form.name.data
            project.server = form.server.data
            project.header = form.header.data
            project.info = form.info.data
            project.progress = 0
            project.type = ProjectTypeEnum(form.type.data)
            project.user_id = get_current_user().id
            project.running = False
            db.session.add(project)
            db.session.flush()
            if form.users.data:
                for user in form.users.data:
                    user_auth = UserAuth()
                    user_auth.user_id = user
                    user_auth.auth_id = project.id
                    user_auth.type = UserAuthEnum.PROJECT
                    db.session.add(user_auth)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UnknownException(msg='新增异常 数据已回滚')

        return True

    @classmethod
    def get_all(cls):
        projects = cls.query.filter_by(delete_time=None) \
            .order_by(text('Project.running desc'), text('Project.update_time desc')).all()
        db.session.execute('reset query cache')
        return projects

    @classmethod
    def search(cls, name):
        projects = cls.query.filter(cls.name.like(f'%{name}%') if name is not None else '',
                                    cls.delete_time == None)\
            .order_by(text('Project.running desc'), text('Project.update_time desc')).all()
        return projects

    @classmethod
    def get_auth(cls):
        """获取当前用户授权的工程 如果登陆用户是管理员则返回多有用例组"""
        if current_user.is_admin:
            projects = cls.get_all()
        else:
            auths = UserAuth.query.filter_by(user_id=current_user.id, _type=UserAuthEnum.PROJECT.value).all()
            pids = [auth.auth_id for auth in auths]
            projects = cls.query.filter(cls.delete_time == None, cls.id.in_(pids)).all()
        if not projects:
            raise NotFound(msg='暂无已授权的工程')
        return projects

    # 判断用户是否有工程的权限
    def user_id_auth(self):
        if not current_user.is_admin:
            auth = UserAuth.query.filter_by(user_id=current_user.id,
                                            _type=UserAuthEnum.PROJECT.value, auth_id=self.id).first()
            if not auth:
                raise Forbidden(msg='无操作此工程的权限')

    @classmethod
    def edit_project(cls, pid, form):
        pid = int(pid)
        project = cls.query.filter_by(id=pid, delete_time=None).first_or_404()
        project.is_running()
        project.user_id_auth()
        # name 组内唯一 此处判断不允许重复
        project_by_name = cls.query.filter_by(name=form.name.data, delete_time=None).first()
        # 获取目标分组当前的授权人员
        old_user_auth = UserAuth.query.filter_by(auth_id=pid, _type=UserAuthEnum.PROJECT.value).all()
        old_users = [user.user_id for user in old_user_auth]
        # 新的授权人员
        new_users = form.users.data
        if project_by_name == project or project_by_name is None:
            try:
                project.id = pid
                project.name = form.name.data
                project.server = form.server.data
                project.header = form.header.data
                project.info = form.info.data
                # 维护人
                project.user_id = current_user.id
                if form.users.data is not None:
                    # 旧人员列表中有 新人员列表中没有，这部分删除
                    old = list(set(old_users).difference(set(new_users)))
                    if old:
                        for user_id in old:
                            user = UserAuth.query.filter_by(user_id=user_id, _type=UserAuthEnum.PROJECT.value,
                                                            auth_id=pid).first_or_404()
                            db.session.delete(user)
                    # 新人员列表中有 旧人员列表中没有，这部分新增
                    new = list(set(new_users).difference(set(old_users)))
                    if new:
                        for user_id in new:
                            user_auth = UserAuth()
                            user_auth.user_id = user_id
                            user_auth.auth_id = pid
                            user_auth.type = UserAuthEnum.PROJECT
                            db.session.add(user_auth)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                raise UnknownException(msg='新增异常请检查数据重试')
        elif project_by_name is not None:
            raise ParameterException(msg='工程已存在')

        return True

    @classmethod
    def remove_project(cls, pid):
        project = cls.query.filter_by(id=pid, delete_time=None).first_or_404()
        project.is_running()
        project.user_id_auth()

        try:
            # 删除分组用户权限表，物理删除
            user_auth = UserAuth.query.filter_by(auth_id=pid, _type=UserAuthEnum.PROJECT.value).all()
            if user_auth:
                users = [user.user_id for user in user_auth]
                for user in users:
                    user = UserAuth.query.filter_by(user_id=user, _type=UserAuthEnum.PROJECT.value, auth_id=pid).first()
                    db.session.delete(user)
            # 删除工程，逻辑删除
            project.delete_time = datetime.now()
            # 删除副本工程配置表 物理删除
            copyConfigs = ConfigCopy.query.filter_by(project_id=pid).all()
            for config in copyConfigs:
                db.session.delete(config)
            # 删除关联工程配置表 物理删除
            relationConfigs = ConfigRelation.query.filter_by(project_id=pid).all()
            for config in relationConfigs:
                db.session.delete(config)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise UnknownException(msg='删除异常请重试')
        return True

    # 工程运行中无法操作
    def is_running(self):
        if self.running:
            raise ProjectConfigException(msg='工程正在运行中无法操作')

    # 保存工程配置
    def save_config(self, configs):
        self.is_running()

        if self.type == ProjectTypeEnum.COPY.value:
            ConfigCopy.copy_config(self.id, configs)
        elif self.type == ProjectTypeEnum.RELATION.value:
            ConfigRelation.relation_config(self.id, configs)

    # 获取配置
    def get_configs(self):
        if self.type == ProjectTypeEnum.COPY.value:
            return ConfigCopy.get_configs(self.id)
        elif self.type == ProjectTypeEnum.RELATION.value:
            return ConfigRelation.get_configs(self.id)

    # 批量执行用例
    def batch(self):
        if self.type == ProjectTypeEnum.COPY.value:
            ConfigCopy.batch(self)
        elif self.type == ProjectTypeEnum.RELATION.value:
            ConfigRelation.batch(self)
        # 执行完毕将结果广播给客户端
        res = requests.get(url='http://127.0.0.1:5000/v1/task/finish/' + str(self.id))
        current_app.logger.debug(res.text)

    # 更新进度
    def update_progress(self, progress, running=None):
        if running is not None:
            self.running = running
        self.progress = progress
        db.session.commit()
        # 将执行进度广播给客户端
        res = requests.get(url='http://127.0.0.1:5000/v1/task/progress')
        current_app.logger.debug(res.text)
