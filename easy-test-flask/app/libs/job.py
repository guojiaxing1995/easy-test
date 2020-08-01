import os
import re
from os import walk
from os import path
from app.libs.tasks import execute_test


# 批量执行job
def execute_job(pid, scheduler_id):
    execute_test.delay(pid, 0, scheduler_id)


# 删除指定目录下某一类型的文件
def delete_file(relative_project_path, reguler):

    file_dir = os.path.join(r'D:\pythonProgram\easy-test\easy-test-flask', relative_project_path)
    for parent, dirNames, fileNames in walk(file_dir):
        for fileName in fileNames:
            r = reguler
            res = re.search(r, fileName)
            os.remove(path.join(parent, fileName)) if res else 1
