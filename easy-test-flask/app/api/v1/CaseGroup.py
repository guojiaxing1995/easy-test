""" 
@Time    : 2020/3/14 10:13
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : CaseGroup.py
@Desc    :
"""
from flask import jsonify
from lin import login_required, route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.CaseGroup import CaseGroup
from app.validators.CaseForm import CaseGroupForm

case_group_api = Redprint('caseGroup')


@case_group_api.route('', methods=['POST'])
@login_required
def create_group():
    form = CaseGroupForm().validate_for_api()
    CaseGroup.new_group(form)
    return Success(msg='新建分组成功')


@case_group_api.route('', methods=['GET'])
@route_meta('用例分组', module='用例')
@group_required
def get_groups():
    groups = CaseGroup.get_all()
    return jsonify(groups)


@case_group_api.route('/<gid>', methods=['PUT'])
@login_required
def update_group(gid):
    form = CaseGroupForm().validate_for_api()
    CaseGroup.edit_group(gid, form)
    return Success(msg='更新分组成功')


@case_group_api.route('/<gid>', methods=['DELETE'])
@route_meta('删除用例分组', module='用例')
@group_required
def delete_group(gid):
    CaseGroup.remove_group(gid)
    return Success(msg='删除分组成功')


@case_group_api.route('/auth', methods=['GET'])
@login_required
def get_auth_groups():
    """获取当前登陆用户的授权分组"""
    groups = CaseGroup.get_auth()
    return jsonify(groups)
