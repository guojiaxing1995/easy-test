from flask import jsonify
from lin import route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.scheduler import Scheduler
from app.validators.SchedulerForm import SchedulerForm, SchedulerSearchForm, SchedulerOperateForm, SchedulerEditForm

scheduler_api = Redprint('scheduler')


@scheduler_api.route('/add', methods=['POST'])
@route_meta('新增定时任务', module='定时任务')
@group_required
def add_job():
    form = SchedulerForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.new_job(form.project.data, form.user.data, form.sendEmail.data, form.copyPerson.data, form.cron.data)

    return Success('新增定时任务成功')


@scheduler_api.route('/search', methods=['GET'])
@route_meta('定时任务列表', module='定时任务')
@group_required
def search_jobs():
    form = SchedulerSearchForm().validate_for_api()
    jobs = Scheduler.search_jobs(form.project.data, form.user.data, form.page.data, form.count.data)
    return jsonify(jobs)


@scheduler_api.route('/start', methods=['GET'])
@route_meta('启动定时任务', module='定时任务')
@group_required
def start_job():
    form = SchedulerOperateForm().validate_for_api()
    scheduler = Scheduler.query.filter_by(scheduler_id=form.schedulerId.data).first()
    scheduler.start_job()

    return Success(msg='启动成功')


@scheduler_api.route('/stop', methods=['GET'])
@route_meta('停止定时任务', module='定时任务')
@group_required
def stop_job():
    form = SchedulerOperateForm().validate_for_api()
    scheduler = Scheduler.query.filter_by(scheduler_id=form.schedulerId.data).first()
    scheduler.stop_job()

    return Success(msg='停止成功')


@scheduler_api.route('/edit/<sid>', methods=['PUT'])
@route_meta('编辑定时任务', module='定时任务')
@group_required
def edit_job(sid):
    form = SchedulerEditForm().validate_for_api()
    scheduler = Scheduler.query.filter_by(id=sid, delete_time=None).first()
    scheduler.edit_job(form.user.data, form.sendEmail.data, form.copyPerson.data, form.cron.data)
    return Success(msg='修改成功')


@scheduler_api.route('/remove/<sid>', methods=['DELETE'])
@route_meta('删除定时任务', module='定时任务')
@group_required
def remove_job(sid):
    scheduler = Scheduler.query.filter_by(id=sid, delete_time=None).first()
    scheduler.remove_job()
    return Success(msg='删除成功')
