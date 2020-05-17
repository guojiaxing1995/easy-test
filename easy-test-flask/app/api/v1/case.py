"""
@Time    : 2020/3/21 10:36
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 用例视图
"""
from flask import jsonify, current_app
from lin import manager
from lin.exception import NotFound, Success, ParameterException
from lin.redprint import Redprint
from lin import route_meta, group_required, login_required

from app.libs.enums import CaseMethodEnum, CaseSubmitEnum, CaseDealEnum, CaseTypeEnum, CaseAssertEnum
from app.models.UserAuth import UserAuth
from app.models.case import Case
from app.validators.CaseForm import UserGroupAuthForm, CaseForm, CaseSearchForm, EnumTypeForm, CaseDebugForm, \
    CaseLogsSearchForm

case_api = Redprint('case')


@case_api.route('', methods=['POST'])
@route_meta('新增用例', module='用例')
@group_required
def create_case():
    form = CaseForm().validate_for_api()
    case = Case(form.caseGroup.data, form.name.data, form.info.data, form.url.data, form.method.data, form.submit.data,
                form.header.data, form.data.data, form.deal.data, form.condition.data, form.expect.data,
                form.assertion.data, form.type.data)
    case.new_case()
    return Success(msg='新增用例成功')


@case_api.route('/<cid>', methods=['PUT'])
@route_meta('编辑用例', module='用例')
@group_required
def update_case(cid):
    form = CaseForm().validate_for_api()
    case = Case.query.filter_by(id=cid, case_group=form.caseGroup.data, delete_time=None).first_or_404()
    case.edit_case(form.name.data, form.info.data, form.url.data, form.method.data, form.submit.data, form.header.data,
                   form.data.data, form.deal.data, form.condition.data, form.expect.data, form.assertion.data,
                   form.type.data)
    return Success(msg='更新用例成功')


@case_api.route('/<cid>', methods=['DELETE'])
@route_meta('删除用例', module='用例')
@group_required
def delete_case(cid):
    case = Case.query.filter_by(id=cid, delete_time=None).first_or_404()
    case.remove_case()
    return Success(msg='删除用例成功')


@case_api.route('', methods=['GET'])
@route_meta('测试用例', module='用例')
@group_required
def get_case():
    form = CaseSearchForm().validate_for_api()
    result = Case.search_case(form.name.data, form.url.data, form.caseGroup.data, form.start.data, form.end.data,
                              form.id.data, form.method.data, form.deal.data, form.page.data, form.count.data)

    return jsonify(result)


@case_api.route('/type', methods=['GET'])
@login_required
def enum_type():
    form = EnumTypeForm().validate_for_api()
    if form.type.data == 'METHOD':
        return CaseMethodEnum.data()
    elif form.type.data == 'SUBMIT':
        return CaseSubmitEnum.data()
    elif form.type.data == 'DEAL':
        return CaseDealEnum.data()
    elif form.type.data == 'TYPE':
        return CaseTypeEnum.data()
    elif form.type.data == 'ASSERT':
        return CaseAssertEnum.data()
    else:
        return {
            'METHOD': CaseMethodEnum.data(),
            'SUBMIT': CaseSubmitEnum.data(),
            'DEAL': CaseDealEnum.data(),
            'TYPE': CaseTypeEnum.data(),
            'ASSERT': CaseAssertEnum.data(),
        }


@case_api.route('/debug', methods=['POST'])
@login_required
def debug():
    form = CaseDebugForm().validate_for_api()
    case = Case(None, None, None, form.url.data, form.method.data, form.submit.data, form.header.data, form.data.data)
    result = case.case_debug()
    return jsonify(result)


@case_api.route('/casesByGroup', methods=['GET'])
@login_required
def cases_by_group():
    form = CaseSearchForm().validate_for_api()
    cases = Case.cases_by_group(form.caseGroup.data)
    return jsonify(cases)


@case_api.route('/logs', methods=['POST'])
@route_meta('用例日志列表', module='测试结果')
@group_required
def case_logs():
    form = CaseLogsSearchForm().validate_for_api()
    cases = Case.case_log_search(form.name.data, form.url.data, form.project.data, form.task.data,
                                 form.result.data, form.start.data, form.end.data, form.count.data, form.page.data)
    return jsonify(cases)


@case_api.route('/logs/delete', methods=['DELETE'])
@route_meta('删除用例日志', module='测试结果')
@group_required
def case_logs_delete():
    form = CaseLogsSearchForm().validate_for_api()
    count = Case.case_log_remove(form.name.data, form.url.data, form.project.data, form.task.data,
                                 form.result.data, form.start.data, form.end.data)
    if count == 0:
        return Success(msg='无符合条件数据')
    else:
        return Success(msg='成功删除' + str(count) + '条数据')
