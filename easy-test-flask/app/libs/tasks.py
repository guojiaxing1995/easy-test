import sys
import time

from flask import current_app
from flask_mail import Message
from lin import manager

from app.libs.enums import EmailStrategyEnum
from app.libs.init import celery, mail
from app.models.project import Project
from celery.utils import log

from app.models.task import Task

sys.path.append('../../')

celery.conf.update(imports='app.libs.tasks')


@celery.task
def execute_test(pid, create_user_id, scheduler_id=None):
    # 初始化工程进度
    project = Project.query.filter_by(id=pid, delete_time=None).first_or_404()
    project.update_progress(progress=0, running=True)
    try:
        project.batch(create_user_id, scheduler_id)
        log.logger.info('任务执行完成')
    finally:
        time.sleep(3)
        project.update_progress(progress=0, running=False)
    return True


@celery.task
def send_text_email(task_id, project_id, scheduler_id):
    task = Task.query.filter_by(id=task_id).first()
    # 判断测试结果
    if task.total == task.success and task.total > 0:
        task_result = True
    else:
        task_result = False

    project = Project.query.filter_by(id=project_id).first()
    if scheduler_id:
        from app.models.scheduler import Scheduler
        scheduler = Scheduler.query.filter_by(scheduler_id=scheduler_id).first()
        if scheduler.send_email:
            if EmailStrategyEnum(scheduler.email_strategy) == EmailStrategyEnum.SUCCESS and task_result is True:
                is_send = True
            elif EmailStrategyEnum(scheduler.email_strategy) == EmailStrategyEnum.FAIL and task_result is False:
                is_send = True
            elif EmailStrategyEnum(scheduler.email_strategy) == EmailStrategyEnum.ALL:
                is_send = True
            else:
                is_send = False
        else:
            is_send = False

        # 收件人
        user = manager.user_model.query.filter_by(id=scheduler.user).first()
        # 抄送人 邮件列表
        copy_person_email = [manager.user_model.query.filter_by(id=uid).first().email
                             for uid in scheduler.copy_person.split(',')] if scheduler.copy_person else []
    else:
        if project.send_email:
            if EmailStrategyEnum(project.email_strategy) == EmailStrategyEnum.SUCCESS and task_result is True:
                is_send = True
            elif EmailStrategyEnum(project.email_strategy) == EmailStrategyEnum.FAIL and task_result is False:
                is_send = True
            elif EmailStrategyEnum(project.email_strategy) == EmailStrategyEnum.ALL:
                is_send = True
            else:
                is_send = False
        else:
            is_send = False

        # 收件人
        user = manager.user_model.query.filter_by(id=project.user).first()
        # 抄送人 邮件列表
        copy_person_email = [manager.user_model.query.filter_by(id=uid).first().email
                             for uid in project.copy_person.split(',')] if project.copy_person else []

    # 不发送邮件
    if not is_send:
        return

    file, directory, filename = task.build_report()

    msg = Message(
        subject='接口自动化测试(' + project.name + ')',
        html=user.username + ',你好：<br><br><p style="text-indent: 2em;">接口自动化测试已完成，测试工程为' + project.name +
                '</p><br><br><p style="text-indent: 2em;">运行用例总数：<span style="color:#3963BC;font-weight:600">' +
                str(task.total) + '</span>，其中通过数：<span style="color:#00C292;font-weight:600">' + str(task.success) +
                '</span>，不通过数：<span style="color:#E46A76;font-weight:600">' + str(task.fail) +
                '</span>,通过率 ' + str(round(task.success / task.total, 2) * 100) +
                '%</p><br><br><p style="text-indent: 2em;">此次测试由' +
                manager.user_model.query.filter_by(id=task.create_user).first().username +
                '执行</p><br><br><span style="color:#CCCCCC">此邮件由接口自动化平台发送，请勿回复~</span>',
        sender=("自动化测试平台", '15234093915@sina.cn'),
        recipients=[user.email],
        cc=copy_person_email
    )
    # 将html报告加入附件
    with current_app.open_resource(file) as f:
        msg.attach(filename, 'html/htm', f.read())
    f.close()
    mail.send(msg)
    log.logger.info('邮件发送成功')
