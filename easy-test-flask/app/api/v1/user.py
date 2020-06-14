from flask import jsonify
from lin import login_required
from lin.redprint import Redprint

from app.models.case import Case
from app.models.project import Project
from app.models.scheduler import Scheduler
from app.models.task import Task
from app.validators.MineForm import MineSearchForm

user_api = Redprint('user')


# 我创建的用例
@user_api.route('/case', methods=['GET'])
@login_required
def case():
    form = MineSearchForm().validate_for_api()
    cases = Case.user_case(form.uid.data, form.name.data, form.page.data, form.count.data)
    return jsonify(cases)


# 我维护的工程
@user_api.route('/project', methods=['GET'])
@login_required
def project():
    form = MineSearchForm().validate_for_api()
    projects = Project.user_project(form.uid.data, form.name.data, form.page.data, form.count.data)
    return jsonify(projects)


# 我维护的定时任务
@user_api.route('/scheduler', methods=['GET'])
@login_required
def scheduler():
    form = MineSearchForm().validate_for_api()
    schedulers = Scheduler.user_scheduler(form.uid.data, form.name.data, form.page.data, form.count.data)
    return jsonify(schedulers)


# 我执行的记录
@user_api.route('/task', methods=['GET'])
@login_required
def task():
    form = MineSearchForm().validate_for_api()
    tasks = Task.user_task(form.uid.data, form.name.data, form.start.data, form.end.data, form.page.data,
                           form.count.data)
    return jsonify(tasks)
