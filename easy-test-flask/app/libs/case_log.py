import time

from flask_jwt_extended import current_user

from app.libs.enums import CaseAssertEnum, CaseTypeEnum, CaseDealEnum, CaseSubmitEnum, CaseMethodEnum, ProjectTypeEnum


def log(case, project, task, user):
    case_log = {
        'id': case.id,
        'case_group': case.case_group,
        'case_group_name': case.case_group_name,
        'name': case.name,
        'actual_result': case.actual_result,
        'assertion_text': CaseAssertEnum.data()[case.assertion],
        'assertion': case.assertion,
        'condition': case.condition,
        'create_time': task.create_time,
        # celery 中获取不到当前用户  只能从dealy传入
        'create_user': user.id,
        'username': user.username,
        'data': case.data,
        'deal_text': CaseDealEnum.data()[case.deal],
        'deal': case.deal,
        'expect': case.expect,
        'header': case.header,
        'info': case.info,
        'method_text': CaseMethodEnum.data()[case.method],
        'method': case.method,
        'reason': case.reason,
        'submit_text': CaseSubmitEnum.data()[case.submit],
        'submit': case.submit,
        'type': CaseTypeEnum.data()[case.type],
        'url': case.url,
        'result': case.result,
        'project_id': project.id,
        'project_name': project.name,
        'project_type': project.type,
        'project_type_name': ProjectTypeEnum.data()[project.type],
        'task_id': task.id,
        'task_no': task.task_no
    }
    return case_log


def log_format(case_log):
    return {
        'id': case_log['id'],
        'case_group': case_log['case_group'],
        'case_group_name': case_log['case_group_name'],
        'name': case_log['name'],
        'actual_result': case_log['actual_result'],
        'assertion_text': case_log['assertion_text'],
        'assertion': case_log['assertion'],
        'condition': case_log['condition'],
        'create_time': case_log['create_time'],
        'create_user': case_log['create_user'],
        'username': case_log['username'],
        'data': case_log['data'],
        'deal_text': case_log['deal_text'],
        'deal': case_log['deal'],
        'expect': case_log['expect'],
        'header': case_log['header'],
        'info': case_log['info'],
        'method_text': case_log['method_text'],
        'method': case_log['method'],
        'reason': case_log['reason'],
        'submit_text': case_log['submit_text'],
        'submit': case_log['submit'],
        'type': case_log['type'],
        'url': case_log['url'],
        'result': case_log['result'],
        'project_id': case_log['project_id'],
        'project_name': case_log['project_name'],
        'project_type': case_log['project_type'],
        'project_type_name': case_log['project_type_name'],
        'task_id': case_log['task_id'],
        'task_no': case_log['task_no']
    }


def edit_log(id, name, info, url, method, submit, header, data, deal, condition, expect, assertion, type, case_group):
    return {
        'id': id,
        'name': name,
        'info': info,
        'url': url,
        'method': method,
        'submit': submit,
        'header': header,
        'data': data,
        'deal': deal,
        'condition': condition,
        'expect': expect,
        'assertion': assertion,
        'type': type,
        'case_group': case_group,
        'create_user': current_user.id,
        'create_user_name': current_user.username,
        'create_time': int(round(time.time() * 1000)),
    }
