import sys
import time


from app.libs.init import celery
from app.models.project import Project
from celery.utils import log

sys.path.append('../../')


celery.conf.update(imports='app.libs.tasks')


@celery.task
def execute_test(pid):
    # 初始化工程进度
    project = Project.query.filter_by(id=pid, delete_time=None).first_or_404()
    project.update_progress(progress=0, running=True)
    try:
        project.batch()
        log.logger.info('任务执行完成')
    finally:
        time.sleep(3)
        project.update_progress(progress=0, running=False)
    return True
