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
