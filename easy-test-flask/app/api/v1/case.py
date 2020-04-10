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
from app.validators.CaseForm import UserGroupAuthForm, CaseForm, CaseSearchForm, EnumTypeForm, CaseDebugForm

case_api = Redprint('case')

#按照用户权限分组返回所有用户 并显示目标类型权限授权情况
@case_api.route('/UserByGroup', methods=['GET'])
@login_required
def users_by_group():
    form = UserGroupAuthForm().validate_for_api()

    user_groups = manager.group_model.get(one=False)
    if user_groups is None:
        raise NotFound(msg='不存在任何用户组')

    for user_group in user_groups:
        users = manager.user_model.query.filter().filter_by(group_id=user_group.id).all()
        if users:
            for user in users:
                # 如果传入权限分组和权限类型则返回对应用户是否获取到授权
                if form.authId.data:
                    # 查询权限表看当前循环用户是否有权限
                    auth = UserAuth.get_user_auth(user.id, form.authId.data, form.authType.data)
                    if auth:
                        setattr(user, 'permission', True)
                        user._fields.append('permission')
                    else:
                        setattr(user, 'permission', False)
                        user._fields.append('permission')
                else:
                    setattr(user, 'permission', False)
                    user._fields.append('permission')
                user.hide('active','admin','group_id','update_time','create_time')
            setattr(user_group, 'users', users)
            user_group._fields.append('users')

    return jsonify(user_groups)

@case_api.route('', methods=['POST'])
@route_meta('新增用例', module='用例')
@group_required
def create_case():
    form = CaseForm().validate_for_api()
    case = Case(form.caseGroup.data,form.name.data,form.info.data,form.url.data,form.method.data,form.submit.data,
                form.header.data,form.data.data,form.deal.data,form.condition.data,form.expectResult.data,form.caseAssert.data,form.type.data)
    case.new_case()
    return Success(msg='新增用例成功')

@case_api.route('/<cid>', methods=['PUT'])
@route_meta('编辑用例', module='用例')
@group_required
def update_case(cid):
    form = CaseForm().validate_for_api()
    case = Case.query.filter_by(id=cid, case_group=form.caseGroup.data, delete_time=None).first_or_404()
    case.edit_case(form.name.data,form.info.data,form.url.data,form.method.data,form.submit.data,form.header.data,
                   form.data.data,form.deal.data,form.condition.data,form.expectResult.data,form.caseAssert.data,form.type.data)
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
    result = Case.search_case(form.name.data,form.url.data,form.caseGroup.data,form.start.data,form.end.data,form.id.data,form.page.data,form.count.data)

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
        raise ParameterException(msg='无目标类型')

@case_api.route('/debug', methods=['POST'])
@login_required
def debug():
    form = CaseDebugForm().validate_for_api()
    case = Case(None,None,None,form.url.data,form.method.data,form.submit.data,form.header.data,form.data.data)
    result = case.case_debug()
    return jsonify(result)
