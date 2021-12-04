import os
import shutil
from datetime import datetime

import requests
from flask import current_app
from flask_jwt_extended import current_user
from lin import db, manager
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, text

from app.libs.error_code import RecordRemoveException
from app.libs.init import mongo
from app.libs.utils import paging
from app.models.case import Case


class Task(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='任务id')
    task_no = Column(String(20), comment='任务编号')
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

    def update_task_no(self):
        self.task_no = self._create_time.strftime("%Y%m%d%H%M%S") + '_' + str(self.project_id)
        db.session.commit()

    def update_result(self, success=None, fail=None):
        if success is not None:
            self.success = success
        if fail is not None:
            self.fail = fail
        db.session.commit()

        # 将执行结果广播给客户端
        api_server = current_app.config.get('API_SERVER')
        res = requests.get(url=api_server + '/v1/task/task/' + str(self.project_id))
        current_app.logger.debug(res.text)

    @classmethod
    def all_tasks(cls, project):
        tasks = cls.query.filter(
            cls.project_id == project if project else '',
            cls.delete_time == None,
        ).order_by(
            text('update_time desc')
        ).all()

        for task in tasks:
            create_user = manager.user_model.query.filter_by(id=task.create_user).first()
            setattr(task, 'create_user_name', create_user.username)
            task._fields.append('create_user_name')
            setattr(task, 'global_var', task.get_global_var())
            task._fields.append('global_var')
        return tasks

    @classmethod
    def get_tasks(cls, user, project, no, start, end, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        results = cls.query.filter(
            cls.create_user == user if user else '',
            cls.project_id == project if project else '',
            cls.task_no.like(f'%{no}%') if no is not None else '',
            cls._create_time.between(start, end) if start and end else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.task_no,
            cls.project_id,
            cls.create_user,
            cls.total,
            cls.success,
            cls.fail,
            cls._create_time.label('create_time')
        ).order_by(
            text('update_time desc')
        ).paginate(page, count)

        items = [dict(zip(result.keys(), result)) for result in results.items]
        for item in items:
            # 获取工程名称
            from app.models.project import Project
            project_name = Project.query.filter_by(id=item['project_id']).first()
            item['project_name'] = project_name.name
            # 获取执行人名称
            user = manager.user_model.query.filter_by(id=item['create_user']).first()
            item['username'] = user.username
            item['create_time'] = int(round(item['create_time'].timestamp() * 1000))
        results.items = items
        data = paging(results)
        return data

    @classmethod
    def delete_tasks(cls, user, project, no, start, end):
        tasks = cls.query.filter(
            cls.create_user == user if user else '',
            cls.project_id == project if project else '',
            cls.task_no.like(f'%{no}%') if no is not None else '',
            cls._create_time.between(start, end) if start and end else '',
            cls.delete_time == None,
        ).all()
        task_no_list = [task.task_no for task in tasks]
        try:
            for task in tasks:
                task.delete_time = datetime.now()
            db.session.commit()
            # 删除task全局变量
            [mongo.db.task.delete_one({'task_id': task.id}) for task in tasks]
            # 删除日志
            for task_no in task_no_list:
                Case.case_log_remove(name=None, url=None, project=None, task=task_no, result=None, start=None, end=None)
        except Exception:
            db.session.rollback()
            raise RecordRemoveException()

        return len(tasks)

    @classmethod
    def user_task(cls, uid, name, start, end, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        from app.models.project import Project
        if not uid:
            uid = current_user.id
        results = cls.query.join(Project, Project.id == cls.project_id).filter(
            cls.create_user == uid,
            Project.name.like(f'%{name}%') if name is not None else '',
            cls._create_time.between(start, end) if start and end else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.task_no,
            cls.project_id,
            cls.create_user,
            cls.total,
            cls.success,
            cls.fail,
            cls._create_time.label('create_time')
        ).order_by(
            text('Task.update_time desc')
        ).paginate(page, count)

        items = [dict(zip(result.keys(), result)) for result in results.items]
        for item in items:
            # 获取工程名称
            from app.models.project import Project
            project_name = Project.query.filter_by(id=item['project_id']).first()
            item['project_name'] = project_name.name
            # 获取执行人名称
            user = manager.user_model.query.filter_by(id=item['create_user']).first()
            item['username'] = user.username
            item['create_time'] = int(round(item['create_time'].timestamp() * 1000))
        results.items = items
        data = paging(results)
        return data

    # 获取今日执行得测试次数、测试得工程数
    @classmethod
    def today(cls):

        execute_task = db.session.execute("SELECT * FROM `easy-test`.`task` where delete_time is null "
                                          "and DATE_FORMAT(create_time,'%Y-%m-%d') = DATE_FORMAT(NOW(),'%Y-%m-%d')")

        execute_project = db.session.execute("SELECT project_id, count(*) FROM `easy-test`.`task` WHERE delete_time IS "
                                             "NULL AND DATE_FORMAT( create_time, '%Y-%m-%d' ) = "
                                             "DATE_FORMAT( NOW( ), '%Y-%m-%d' ) GROUP BY project_id")

        return len(list(execute_task)), len(list(execute_project))

    def copy_report_template(self):
        template_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/document/report/template'
        download_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/document/report/download'
        if not os.path.exists(download_directory):
            os.makedirs(download_directory)
        template_filename = 'report.html'
        from app.models.project import Project
        project = Project.query.filter_by(id=self.project_id).first()
        download_filename = 'report_' + project.name + '.html'
        # 复制用例下载模板作为被写入的文件
        shutil.copyfile(template_directory + '/' + template_filename, download_directory + '/' + download_filename)

        return download_directory + '/' + download_filename, download_directory, download_filename

    def build_report(self):
        # 测试时间
        report_time = self._create_time.strftime("%Y-%m-%d %H:%M")
        # 被测试工程
        from app.models.project import Project
        project = Project.query.filter_by(id=self.project_id).first()
        # 测试人员
        tester = manager.user_model.query.filter_by(id=self.create_user).first()
        # task 成功个数
        if self.success:
            input_success = '<input checked="true" class="filter" data-test-result="passed" hidden="true" ' \
                            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/><span ' \
                            'class="passed">' + str(self.success) + ' passed</span>'
        else:
            input_success = '<input checked="true" class="filter" disabled="true" data-test-result="passed" ' \
                            'hidden="true" name="filter_checkbox" onChange="filter_table(this)" ' \
                            'type="checkbox"/><span class="passed">' + str(self.success) + ' passed</span>'
        # task 失败个数
        if self.fail:
            input_fail = '<input checked="true" class="filter" data-test-result="failed" hidden="true" ' \
                         'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/><span ' \
                         'class="failed">' + str(self.fail) + ' passed</span>'
        else:
            input_fail = '<input checked="true" class="filter" disabled="true" data-test-result="failed" ' \
                         'hidden="true" name="filter_checkbox" onChange="filter_table(this)" ' \
                         'type="checkbox"/><span class="failed">' + str(self.fail) + ' failed</span>'
        # 用例记录
        logs = Case.case_log_search_all(self.task_no)
        table_logs = ''
        for log in logs:
            result = 'Passed' if log['actual_result'] else 'Failed'
            expect = log['expect'] if log['expect'] else ''
            interface_return = log['result']['text'] if log['result'] else ''
            if log['actual_result']:
                table_tr = '<tbody class="passed results-table-row"><tr><td class="col-result">' + result + \
                           '</td><td class="col-name">' + log['name'] + \
                           '</td><td class="col-method">' + log['method_text'] + '</td><td class="col-url">' + \
                           log['url'] + '</td><td class="col-assertion">' + log['assertion_text'] + \
                           '</td><td class="col-expect">' + expect + \
                           '</td></tr><tr><td class="extra" colspan="6"><div class="empty log">' \
                           + interface_return + '</div></td></tr></tbody>'
            else:
                table_tr = '<tbody class="failed results-table-row"><tr><td class="col-result">' + result + \
                           '</td><td class="col-name">' + log['name'] + \
                           '</td><td class="col-method">' + log['method_text'] + '</td><td class="col-url">' + \
                           log['url'] + '</td><td class="col-assertion">' + log['assertion_text'] + \
                           '</td><td class="col-expect">' + expect + \
                           '</td></tr><tr><td class="extra" colspan="6"><div class="empty log">' \
                           + interface_return + '</div></td></tr></tbody>'
            table_logs = table_logs + table_tr

        download_file, download_directory, download_filename = self.copy_report_template()
        old_file = open(download_file, "r", encoding='utf-8')
        report = old_file.read()
        old_file.close()
        new_file = report.replace('{{ logs }}', table_logs).replace('{{ input_success }}', input_success).replace(
            '{{ input_fail }}', input_fail).replace('{{ project }}', project.name).replace(
            '{{ report_time }}', report_time).replace('{{ tester }}', tester.username)
        with open(download_file, "w", encoding='utf-8') as f:
            f.write(new_file)

        return download_file, download_directory, download_filename

    def get_global_var(self):
        var_data = mongo.db.task.find_one({'task_id': self.id}, {"_id": 0})['global_var'] if \
            mongo.db.task.find_one({'task_id': self.id}) else None

        return var_data

    def set_global_var(self, project):
        # 将vat_dick插入数据库
        mongo.db.task.update_one(
            {'task_id': self.id},
            {'$set': {
                'task_id': self.id,
                'task_no': self.task_no,
                'project_id': project.id,
                'global_var': project.var_dick
            }},
            upsert=True
        )

        # 将执行结果广播给客户端
        api_server = current_app.config.get('API_SERVER')
        res = requests.get(url=api_server + '/v1/task/task/' + str(self.project_id))
        current_app.logger.debug(res.text)
