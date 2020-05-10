from app.libs.enums import CaseAssertEnum, CaseTypeEnum, CaseDealEnum, CaseSubmitEnum, CaseMethodEnum, ProjectTypeEnum


def log(case, project, task, user):
    case_log = {
        'id': case.id,
        'name': case.name,
        'actual_result': case.actual_result,
        'assertion': CaseAssertEnum.data()[case.assertion],
        'condition': case.condition,
        'create_time': task.create_time,
        # celery 中获取不到当前用户
        # 'create_user': user.id,
        # 'username': user.username,
        'data': case.data,
        'deal': CaseDealEnum.data()[case.deal],
        'expect': case.expect,
        'header': case.header,
        'info': case.info,
        'method': CaseMethodEnum.data()[case.method],
        'reason': case.reason,
        'submit': CaseSubmitEnum.data()[case.submit],
        'type': CaseTypeEnum.data()[case.type],
        'url': case.url,
        'result': case.result,
        'project_id': project.id,
        'project_name': project.name,
        'project_type': ProjectTypeEnum.data()[project.type],
        'task_id': task.id
    }
    return case_log
