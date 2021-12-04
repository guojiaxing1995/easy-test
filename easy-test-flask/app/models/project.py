import json
from datetime import datetime

import requests
from flask import current_app
from flask_jwt_extended import current_user, get_current_user
from lin import manager
from lin.db import db
from lin.exception import NotFound, ParameterException, UnknownException, Forbidden
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger, Boolean, text

from app.libs.enums import UserAuthEnum, ProjectTypeEnum, EmailStrategyEnum
from app.libs.error_code import ProjectConfigException, RequestParamException
from app.libs.init import mongo
from app.libs.utils import paging
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
    user = Column(Integer, nullable=False, comment='维护人员')
    send_email = Column(Boolean, nullable=False, default=True, comment='是否发送邮件')
    _email_strategy = Column('email_strategy', SmallInteger, nullable=False, comment='邮件发送策略; 1 -> 总是发送 | '
                                                                                     '2 -> 成功时发送 | 3 ''->失败时发送')
    copy_person = Column(String(50), comment='邮件抄送人员')

    @property
    def type(self):
        return ProjectTypeEnum(self._type).value

    @type.setter
    def type(self, typeEnum):
        self._type = typeEnum.value

    @property
    def email_strategy(self):
        return EmailStrategyEnum(self._email_strategy).value

    @email_strategy.setter
    def email_strategy(self, strategyEnum):
        self._email_strategy = strategyEnum.value

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
            project.user = form.user.data
            project.running = False
            project.send_email = form.sendEmail.data
            project.email_strategy = EmailStrategyEnum(form.emailStrategy.data)
            project.copy_person = form.copyPerson.data
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
        for project in projects:
            # 添加user_name属性
            user_name = manager.user_model.query.filter_by(id=project.user).first().username
            setattr(project, 'user_name', user_name)
            project._fields.append('user_name')

            # 抄送人
            copy_users_name = []
            if project.copy_person:
                for u in project.copy_person.split(','):
                    copy_user = manager.user_model.query.filter_by(id=int(u)).first().username if u else None
                    # 如果用户存在则加入抄送人列表
                    copy_users_name.append(copy_user) if copy_user else 1
            setattr(project, 'copy_person_name', copy_users_name)
            project._fields.append('copy_person_name')

        # 清理查询查询缓存
        db.session.execute('reset query cache')
        return projects

    @classmethod
    def get_all_paginate(cls, name, page, count):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        results = cls.query.filter(
            cls.name.like(f'%{name}%') if name is not None else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.name,
            cls.server,
            cls.header,
            cls.info,
            cls._type.label('type'),
            cls._email_strategy.label('email_strategy'),
            cls.running,
            cls.progress,
            cls.user,
            cls.send_email,
            cls.copy_person,
        ).order_by(text('Project.running desc'), text('Project.update_time desc')).paginate(page, count)

        projects = [dict(zip(result.keys(), result)) for result in results.items]

        for project in projects:
            # 添加user_name属性
            user_name = manager.user_model.query.filter_by(id=project['user']).first().username
            project['user_name'] = user_name

            # 抄送人
            copy_users_name = []
            if project['copy_person']:
                for u in project['copy_person'].split(','):
                    copy_user = manager.user_model.query.filter_by(id=int(u)).first().username if u else None
                    # 如果用户存在则加入抄送人列表
                    copy_users_name.append(copy_user) if copy_user else 1
            project['copy_person_name'] = copy_users_name

        results.items = projects
        data = paging(results)
        return data

    @classmethod
    def search(cls, name):
        projects = cls.query.filter(cls.name.like(f'%{name}%') if name is not None else '',
                                    cls.delete_time == None) \
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
                project.send_email = form.sendEmail.data
                project.email_strategy = EmailStrategyEnum(form.emailStrategy.data)
                project.copy_person = form.copyPerson.data
                # 维护人
                project.user = form.user.data
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
            # 删除工程的用户自定义参数
            project.set_user_parameters()
            # 删除工程对应的定时任务
            from app.models.scheduler import Scheduler
            schedulers = Scheduler.query.filter_by(project_id=project.id, delete_time=None).all()
            for scheduler in schedulers:
                scheduler.remove_job()
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
    def batch(self, create_user_id, scheduler_id):
        # 获取执行用户信息
        task = None
        create_user = manager.user_model.query.filter_by(id=create_user_id).first()
        if self.type == ProjectTypeEnum.COPY.value:
            task = ConfigCopy.batch(self, create_user)
        elif self.type == ProjectTypeEnum.RELATION.value:
            task = ConfigRelation.batch(self, create_user)

        # 执行完毕将结果广播给客户端
        api_server = current_app.config.get('API_SERVER')
        res = requests.get(url=api_server + '/v1/task/finish/' + str(self.id))
        current_app.logger.debug(res.text)

        # 发送邮件
        from app.libs.tasks import send_text_email
        send_text_email.delay(task.id, self.id, scheduler_id)

    # 更新进度
    def update_progress(self, progress, running=None):
        if running is not None:
            self.running = running
        self.progress = progress
        db.session.commit()
        # 将执行进度广播给客户端
        api_server = current_app.config.get('API_SERVER')
        res = requests.get(url=api_server + '/v1/task/progress')
        current_app.logger.debug(res.text)

    # 查询指定用户的工程数据，如果不指定，则查询当前用户
    @classmethod
    def user_project(cls, uid, name, page, count):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        if not uid:
            uid = current_user.id
        results = cls.query.filter(
            cls.user == uid,
            cls.name.like(f'%{name}%') if name is not None else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.name,
            cls.server,
            cls.header,
            cls.info,
            cls._type.label('type'),
            cls.running,
            cls.progress,
            cls.user,
            cls.send_email,
            cls.copy_person,
        ).order_by(text('Project.running desc'), text('Project.update_time desc')).paginate(page, count)

        projects = [dict(zip(result.keys(), result)) for result in results.items]

        for project in projects:
            # 添加user_name属性
            user_name = manager.user_model.query.filter_by(id=project['user']).first().username
            project['user_name'] = user_name

            # 抄送人
            copy_users_name = []
            if project['copy_person']:
                for u in project['copy_person'].split(','):
                    copy_user = manager.user_model.query.filter_by(id=int(u)).first().username if u else None
                    # 如果用户存在则加入抄送人列表
                    copy_users_name.append(copy_user) if copy_user else 1
            project['copy_person_name'] = copy_users_name

        results.items = projects
        data = paging(results)
        return data

    # 工程总数
    @classmethod
    def total(cls):
        return cls.query.filter_by(delete_time=None).count()

    @classmethod
    def rate_top(cls):
        # 工程总成功率top5  总失败率top5

        success_rate = db.session.execute("SELECT project.NAME AS name,FORMAT( AVG( rate ) * 100, 2 ) AS success_rate "
                                          "FROM ( SELECT project_id, success / total AS rate FROM `task` "
                                          "WHERE delete_time IS NULL GROUP BY project_id, success / total ) AS "
                                          "success_rate_first,`project` WHERE project.id = "
                                          "success_rate_first.project_id GROUP BY project_id ORDER BY success_rate "
                                          "DESC LIMIT 5")

        fail_rate = db.session.execute("SELECT project.NAME AS name,FORMAT( AVG( rate ) * 100, 2 ) AS fail_rate "
                                       "FROM( SELECT project_id, fail / total AS rate FROM `task` WHERE delete_time IS "
                                       "NULL GROUP BY project_id, fail / total ) AS fail_rate_first,`project` WHERE "
                                       "project.id = fail_rate_first.project_id GROUP BY project_id ORDER BY fail_rate "
                                       "DESC LIMIT 5")
        return {
            'success_rate': list(success_rate),
            'fail_rate': list(fail_rate),
        }

    def collect(self):
        # 执行总数
        execute_total = db.session.execute("SELECT count( * ) AS total FROM `task` WHERE delete_time IS NULL AND "
                                           "project_id = " + str(self.id))
        try:
            execute_total = list(execute_total)[0]['total']
        except Exception:
            execute_total = 0

        # 成功数
        success_total = db.session.execute("SELECT count( * ) AS total FROM `task` WHERE delete_time IS NULL AND "
                                           "total =success AND success != 0 AND project_id =" + str(self.id))
        try:
            success_total = list(success_total)[0]['total']
        except Exception:
            success_total = 0
        # 当前成功率
        current_success_rate = db.session.execute(text("SELECT FORMAT( success / total * 100, 2 ) AS rate FROM `task` "
                                                       "WHERE delete_time IS NULL AND project_id = :pid ORDER BY "
                                                       "create_time DESC LIMIT 1"),
                                                  {'pid': self.id})
        try:
            current_success_rate = float(list(current_success_rate)[0]['rate'])
        except Exception:
            current_success_rate = 0
        # 上一次成功率
        last_success_rate = db.session.execute(text("SELECT FORMAT( success / total * 100, 2 ) AS rate FROM `task` "
                                                    "WHERE delete_time IS NULL AND project_id = :pid ORDER BY "
                                                    "create_time DESC LIMIT 1,1"),
                                               {'pid': self.id})
        try:
            last_success_rate = float(list(last_success_rate)[0]['rate'])
        except Exception:
            last_success_rate = 0
        # 同比增长
        try:
            yoy_growth = float(format((current_success_rate - last_success_rate) / last_success_rate * 100, '.2f'))
        except Exception:
            yoy_growth = 0

        # 以天为单位的近7次执行记录
        day_execute = []
        # 最近有过执行记录的日期
        last_seven_days = []
        test_date = db.session.execute(text("SELECT DATE_FORMAT( create_time, '%Y-%m-%d' ) as test_date FROM "
                                            "`task` WHERE delete_time IS NULL AND project_id = :pid GROUP BY "
                                            "DATE_FORMAT( create_time, '%Y-%m-%d' ) ORDER BY "
                                            "DATE_FORMAT( create_time, '%Y-%m-%d' ) DESC LIMIT 7"),
                                       {'pid': self.id})
        for i in list(test_date):
            last_seven_days.append(i['test_date'])

        for day in last_seven_days:
            task = db.session.execute(text("SELECT (UNIX_TIMESTAMP(create_time) * 1000) AS create_time,success,fail,"
                                           "total FROM `task` WHERE delete_time IS NULL AND project_id = :pid AND "
                                           "DATE_FORMAT( create_time, '%Y-%m-%d' ) = :day ORDER BY create_time "
                                           "DESC LIMIT 1"),
                                      {'pid': self.id, 'day': day})
            day_execute.append(list(task)[0])
            # 排序
            length = len(day_execute)
            for index in range(length):
                # 标志位
                flag = True
                for j in range(1, length - index):
                    if day_execute[j - 1]['create_time'] > day_execute[j]['create_time']:
                        day_execute[j - 1], day_execute[j] = day_execute[j], day_execute[j - 1]
                        flag = False
                if flag:
                    # 没有发生交换，直接返回list
                    break

        # 雷达图

        # 成功率
        success_rate = db.session.execute(text("SELECT project.NAME,FORMAT( AVG( rate ) * 100, 2 ) AS success_rate "
                                               "FROM( SELECT project_id, success / total AS rate FROM `task` WHERE "
                                               "delete_time IS NULL GROUP BY project_id, success / total ) AS "
                                               "success_rate_first,`project` WHERE project.id = "
                                               "success_rate_first.project_id AND project_id = :pid GROUP BY "
                                               "project_id ORDER BY success_rate DESC"),
                                          {'pid': self.id})
        try:
            success_rate = float(list(success_rate)[0]['success_rate'])
        except Exception:
            success_rate = 0

        # 用例数
        case_count = []
        if self.type == ProjectTypeEnum.COPY.value:
            case_count = db.session.execute(text("SELECT count( * ) AS case_count FROM config_copy WHERE delete_time "
                                                 "IS NULL AND project_id = :pid"),
                                            {'pid': self.id})
        elif self.type == ProjectTypeEnum.RELATION.value:
            case_count = db.session.execute(text("SELECT count( * ) AS case_count FROM config_relation WHERE "
                                                 "delete_time IS NULL AND project_id = :pid"),
                                            {'pid': self.id})
        try:
            case_count = list(case_count)[0]['case_count']
        except Exception:
            case_count = 0

        # 执行天数
        execute_day = db.session.execute(text("SELECT DATE_FORMAT( create_time, '%Y-%m-%d' ) as test_date FROM `task` "
                                              "WHERE delete_time IS NULL AND project_id = :pid GROUP BY "
                                              "DATE_FORMAT( create_time, '%Y-%m-%d' ) "),
                                         {'pid': self.id})
        try:
            execute_day = list(execute_day)[0]['test_date']
        except Exception:
            case_count = 0

        # 执行频率
        try:
            frequency = float(execute_total) / len(execute_day)
        except Exception:
            frequency = 0

        # 定时任务
        scheduler_count = db.session.execute(text("SELECT * FROM scheduler WHERE delete_time IS NULL AND "
                                                  "project_id = :pid"),
                                             {'pid': self.id})
        scheduler_count = len(list(scheduler_count))

        # 执行人数
        tester_count = db.session.execute(text("SELECT create_user FROM `task` WHERE delete_time IS NULL AND "
                                               "project_id = :pid GROUP BY create_user"),
                                          {'pid': self.id})
        tester_count = len(list(tester_count))

        max_success_rate = 100

        max_case_count = 30
        if max_case_count < case_count:
            max_case_count = case_count

        max_frequency = 2
        if max_frequency < frequency:
            max_frequency = frequency

        max_scheduler_count = 1
        if max_scheduler_count < scheduler_count:
            max_scheduler_count = scheduler_count

        max_tester_count = 2
        if max_tester_count < tester_count:
            max_tester_count = tester_count

        radar_chart = {
            'indicator': [{'text': '成功率', 'max': max_success_rate},
                          {'text': '用例数', 'max': max_case_count},
                          {'text': '执行频率', 'max': max_frequency},
                          {'text': '定时任务', 'max': max_scheduler_count},
                          {'text': '测试人数', 'max': max_tester_count}],
            'value': [success_rate, case_count, frequency, scheduler_count, tester_count]
        }

        return {
            'execute_total': execute_total,
            'success_total': success_total,
            'current_success_rate': current_success_rate,
            'yoy_growth': yoy_growth,
            'day_execute': day_execute,
            'radar_chart': radar_chart
        }

    def set_user_parameters(self, parameters=None):
        # param 存在 则为新增/修改 否则为删除
        if parameters:
            if type(parameters) != dict:
                try:
                    parameters = json.loads(parameters.strip())
                except Exception:
                    raise RequestParamException(msg='请填写json格式数据')
            # 如果目标工程设置过参数则更新 否则新增
            mongo.db.project.update_one(
                {'project_id': self.id},
                {'$set': {
                    'project_id': self.id,
                    'parameters': parameters
                }},
                upsert=True
            )
        else:
            mongo.db.project.delete_one({'project_id': self.id})

        return True

    def get_user_parameters(self):
        param = mongo.db.project.find_one({'project_id': self.id}, {"_id": 0})['parameters'] if \
            mongo.db.project.find_one({'project_id': self.id}) else None
        data = {
            'pid': self.id,
            'param': param
        }
        return data
