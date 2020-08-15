import datetime

from flask import current_app
from flask_jwt_extended import current_user
from lin import db, manager
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, Boolean, text, SmallInteger

from app.libs.enums import EmailStrategyEnum
from app.libs.init import scheduler
from app.libs.job import execute_job
from app.libs.utils import paging
from app.models.project import Project


class Scheduler(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键id')
    scheduler_id = Column(String(150), comment='scheduler id')
    project_id = Column(Integer, nullable=False, comment='主键id')
    user = Column(Integer, nullable=False, comment='维护人员')
    send_email = Column(Boolean, nullable=False, default=True, comment='是否发送邮件')
    _email_strategy = Column('email_strategy', SmallInteger, nullable=False, comment='邮件发送策略; 1 -> 总是发送 | '
                                                                                     '2 -> 成功时发送 | 3 ''->失败时发送')
    cron = Column(String(30), nullable=False, comment='cron表达式')
    copy_person = Column(String(50), comment='邮件抄送人员')
    next_run_time = ''
    # 运行状态
    state = True

    @property
    def email_strategy(self):
        return EmailStrategyEnum(self._email_strategy).value

    @email_strategy.setter
    def email_strategy(self, strategyEnum):
        self._email_strategy = strategyEnum.value

    def create_scheduler_id(self):
        project = Project.query.filter_by(id=self.project_id).first_or_404()
        self.scheduler_id = project.name + '_scheduler_' + str(self.id)

    # 数据库添加数据
    def add_scheduler(self, project_id, user, send_email, copy_person, cron, email_strategy):
        self.project_id = project_id
        self.user = user
        self.state = True
        self.send_email = send_email
        self.copy_person = copy_person
        self.cron = cron
        self.email_strategy = EmailStrategyEnum(email_strategy)
        db.session.add(self)
        db.session.flush()
        self.create_scheduler_id()
        db.session.commit()

    def add_job(self):
        [second, minute, hour, day, month, day_of_week, year] = self.cron.split()
        day = None if day == '?' else day
        day_of_week = None if day_of_week == '?' else day_of_week
        current_app.apscheduler.add_job(func=execute_job, args=(self.project_id, self.scheduler_id),
                                        id=self.scheduler_id,
                                        trigger='cron', second=second, minute=minute, hour=hour, day=day, month=month,
                                        day_of_week=day_of_week, year=year, replace_existing=True)

    # 新增任务
    def new_job(self, project_id, user, send_email, copy_person, cron, email_strategy):
        self.add_scheduler(project_id, user, send_email, copy_person, cron, email_strategy)
        self.add_job()

    @classmethod
    def get_jobs(cls):
        jobs = scheduler.get_jobs()
        return jobs

    # 获取任务详情
    @classmethod
    def get_job_detail(cls):
        job_id_list = []
        next_run_time_dict = {}
        jobs = cls.get_jobs()
        for job in jobs:
            job_id_list.append(job.id)
            next_run_time_str = None
            if isinstance(job.next_run_time, datetime.datetime):
                next_run_time_str = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
            next_run_time_dict[job.id] = next_run_time_str
        return job_id_list, next_run_time_dict

    # 获取所有任务
    @classmethod
    def search_jobs(cls, project_id, user_id, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        results = cls.query.filter(
            cls.project_id == project_id if project_id else '',
            cls.user == user_id if user_id else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.scheduler_id,
            cls.project_id,
            cls.user,
            cls.copy_person,
            cls.send_email,
            cls._email_strategy.label('email_strategy'),
            cls.cron,
        ).order_by(
            text('Scheduler.update_time desc')
        ).paginate(page, count)

        jobs = [dict(zip(result.keys(), result)) for result in results.items]

        # 为job添加next_run_time 和 state 属性
        job_id_list, next_run_time_dict = cls.get_job_detail()
        for job in jobs:
            if job['scheduler_id'] in job_id_list:
                job['state'] = True
                job['next_run_time'] = next_run_time_dict[job['scheduler_id']]
                # 如果任务被暂停，置状态为未运行
                if job['next_run_time'] is None:
                    job['state'] = False
            else:
                job['state'] = False
                job['next_run_time'] = None
            # 工程名称
            job['project_name'] = Project.query.filter_by(id=job['project_id']).first().name
            # 维护人名称
            job['user_name'] = manager.user_model.query.filter_by(id=job['user']).first().username
            # 抄送人
            copy_users_name = []
            if job['copy_person']:
                for u in job['copy_person'].split(','):
                    copy_user = manager.user_model.query.filter_by(id=int(u)).first().username if u else None
                    # 如果用户存在则加入抄送人列表
                    copy_users_name.append(copy_user) if copy_user else 1
            job['copy_person_name'] = copy_users_name

        results.items = jobs
        data = paging(results)

        return data

    def start_job(self):
        scheduler.resume_job(self.scheduler_id)

    def stop_job(self):
        scheduler.pause_job(self.scheduler_id)

    def edit_job(self, user, send_email, copy_person, cron, email_strategy):
        old_cron = self.cron
        # cron表达式有变动修改定时任务
        if old_cron != cron:
            self.modify_job(cron)
        self.user = user
        self.send_email = send_email
        self.copy_person = copy_person
        self.cron = cron
        self.email_strategy = EmailStrategyEnum(email_strategy)
        db.session.commit()

    # 修改cron定时任务执行
    def modify_job(self, cron):
        [second, minute, hour, day, month, day_of_week, year] = cron.split()
        day = None if day == '?' else day
        day_of_week = None if day_of_week == '?' else day_of_week
        current_app.apscheduler.modify_job(func=execute_job, args=(self.project_id, self.scheduler_id),
                                           id=self.scheduler_id,
                                           trigger='cron', second=second, minute=minute, hour=hour, day=day,
                                           month=month, day_of_week=day_of_week, year=year)

    def remove_job(self):
        self.delete_time = datetime.datetime.now()
        db.session.commit()
        scheduler.delete_job(self.scheduler_id)

    # 获取所有任务
    @classmethod
    def user_scheduler(cls, uid, name, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        if not uid:
            uid = current_user.id
        results = cls.query.join(Project, Project.id == cls.project_id).filter(
            cls.user == uid,
            Project.name.like(f'%{name}%') if name is not None else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.scheduler_id,
            cls.project_id,
            cls.user,
            cls.copy_person,
            cls.send_email,
            cls.cron,
        ).order_by(
            text('Scheduler.update_time desc')
        ).paginate(page, count)

        jobs = [dict(zip(result.keys(), result)) for result in results.items]

        # 为job添加next_run_time 和 state 属性
        job_id_list, next_run_time_dict = cls.get_job_detail()
        for job in jobs:
            if job['scheduler_id'] in job_id_list:
                job['state'] = True
                job['next_run_time'] = next_run_time_dict[job['scheduler_id']]
                # 如果任务被暂停，置状态为未运行
                if job['next_run_time'] is None:
                    job['state'] = False
            else:
                job['state'] = False
                job['next_run_time'] = None
            # 工程名称
            job['project_name'] = Project.query.filter_by(id=job['project_id']).first().name
            # 维护人名称
            job['user_name'] = manager.user_model.query.filter_by(id=job['user']).first().username
            # 抄送人
            copy_users_name = []
            if job['copy_person']:
                for u in job['copy_person'].split(','):
                    copy_user = manager.user_model.query.filter_by(id=int(u)).first().username if u else None
                    # 如果用户存在则加入抄送人列表
                    copy_users_name.append(copy_user) if copy_user else 1
            job['copy_person_name'] = copy_users_name

        results.items = jobs
        data = paging(results)

        return data

    # 定时任务总数
    @classmethod
    def total(cls):
        return cls.query.filter_by(delete_time=None).count()
