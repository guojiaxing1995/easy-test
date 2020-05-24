import time

from flask import jsonify, current_app, request
from flask_jwt_extended import current_user
from lin import login_required, route_meta, group_required

from app.libs.case_log import log_format
from app.libs.init import socket_io
from lin.exception import Success
from lin.redprint import Redprint

from app.models.case import Case
from app.models.project import Project
from app.models.task import Task
from app.validators.TaskForm import TaskSearchForm

task_api = Redprint('task')


@task_api.route('/<pid>', methods=['GET'])
@login_required
def execute_project(pid):
    project = Project.query.filter_by(id=pid, delete_time=None).first_or_404()
    project.is_running()
    from app.libs.tasks import execute_test
    execute_test.delay(pid, current_user.id)
    return Success(msg='启动成功')


@task_api.route('', methods=['GET'])
@route_meta('运行记录', module='测试结果')
@group_required
def get_tasks():
    form = TaskSearchForm().validate_for_api()
    tasks = Task.get_tasks(form.user.data, form.project.data, form.no.data, form.start.data, form.end.data,
                           form.page.data, form.count.data)

    return jsonify(tasks)


@task_api.route('/all', methods=['GET'])
@login_required
def all_tasks():
    form = TaskSearchForm().validate_for_api()
    tasks = Task.all_tasks(form.project.data)

    return jsonify(tasks)


@task_api.route('/delete', methods=['DELETE'])
@route_meta('删除运行记录', module='测试结果')
@group_required
def delete_tasks():
    form = TaskSearchForm().validate_for_api()
    count = Task.delete_tasks(form.user.data, form.project.data, form.no.data, form.start.data, form.end.data)

    if count == 0:
        return Success(msg='无符合条件数据')
    else:
        return Success(msg='成功删除' + str(count) + '条数据')


# 内部调用   对工程的执行结果进行广播
@task_api.route('/finish/<pid>', methods=['GET'])
def task_over(pid):
    project = Project.query.filter_by(id=int(pid), delete_time=None).first_or_404()
    socket_io.emit('finish', {'name': project.name})
    return Success(msg='广播成功')


# 内部调用   对某一工程的任务记录进行广播
@task_api.route('/task/<pid>', methods=['GET'])
def task_progress(pid):
    tasks = Task.all_tasks(pid)
    task_lists = []
    for task in tasks:
        t = {
            'id': task.id,
            'task_no': task.task_no,
            'project_id': task.project_id,
            'create_user': task.create_user,
            'create_user_name': task.create_user_name,
            'total': task.total,
            'success': task.success,
            'fail': task.fail,
            'create_time': task.create_time,
            'update_time': task.update_time,
        }
        task_lists.append(t)
    socket_io.emit('task', {'tasks': task_lists, 'project_id': int(pid)})
    return Success(msg='广播成功')


# 内部调用   对某一任务编号的日志进行广播
@task_api.route('/log/<taskNo>', methods=['GET'])
def task_log(taskNo):
    logs = Case.case_log_search_all(taskNo)
    logs_lists = []
    for log in logs:
        l = log_format(log)
        logs_lists.append(l)
    socket_io.emit('log', {'logs': logs_lists, 'task_no': taskNo})
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
            'progress': project.progress,
            'running': project.running,
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
