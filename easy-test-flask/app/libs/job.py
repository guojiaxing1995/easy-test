from app.libs.tasks import execute_test


# 批量执行job
def execute_job(pid, scheduler_id):
    execute_test.delay(pid, 0, scheduler_id)
