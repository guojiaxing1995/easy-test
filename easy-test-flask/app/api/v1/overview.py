from flask import jsonify
from lin import route_meta, group_required, login_required
from lin.redprint import Redprint

from app.models.case import Case
from app.models.mock import Mock
from app.models.project import Project
from app.models.scheduler import Scheduler
from app.models.task import Task
from app.models.user import User

overview_api = Redprint('overview')


@overview_api.route('/total', methods=['GET'])
@login_required
def total():
    return {
        'project': Project.total(),
        'case': Case.total(),
        'scheduler': Scheduler.total(),
        'mock': Mock.total()
    }


@overview_api.route('/today', methods=['GET'])
@login_required
def today():
    test_count, test_project_count = Task.today()
    return {
        'case_add_count': Case.today(),
        'test_count': test_count,
        'test_project_count': test_project_count
    }


@overview_api.route('/projectTop', methods=['GET'])
@login_required
def project_top():
    return Project.rate_top()


@overview_api.route('/userTop', methods=['GET'])
@login_required
def user_top():
    return User.execute_top()


@overview_api.route('/caseTop', methods=['GET'])
@login_required
def case_top():
    return Case.top()


@overview_api.route('/project/<pid>', methods=['GET'])
@login_required
def project_collect(pid):
    project = Project.query.filter_by(id=pid).first()
    return project.collect()

