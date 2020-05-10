import time

from flask import jsonify, current_app, request
from lin import login_required

from app.libs.init import socket_io
from lin.exception import Success
from lin.redprint import Redprint

from app.models.project import Project

task_api = Redprint('task')


@task_api.route('/<pid>', methods=['GET'])
@login_required
def execute_project(pid):
    project = Project.query.filter_by(id=pid, delete_time=None).first_or_404()
    project.is_running()
    from app.libs.tasks import execute_test
    execute_test.delay(pid)
    return Success(msg='启动成功')


# 内部调用   对工程的执行结果进行广播
@task_api.route('/finish/<pid>', methods=['GET'])
def task_over(pid):
    project = Project.query.filter_by(id=int(pid), delete_time=None).first_or_404()
    socket_io.emit('finish', {'name': project.name})
    return Success(msg='广播成功')


# 内部调用   对所有工程的执行进度进行广播
@task_api.route('/progress', methods=['GET'])
def progress():
    projects = Project.get_all()
    projects_list = []
    for project in projects:
        p = {
            'id': project.id,
            'name': project.name,
            'progress': project.progress
        }
        projects_list.append(p)
    socket_io.emit('progress', projects_list)
    del projects
    return Success(msg='广播成功')


@socket_io.on('disconnect')
def disconnect():
    current_app.logger.info(request.sid + ' is disconnect')


@socket_io.on('connect')
def connect():
    current_app.logger.info(request.sid + ' is connect')

