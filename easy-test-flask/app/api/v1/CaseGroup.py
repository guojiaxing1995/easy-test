""" 
@Time    : 2020/3/14 10:13
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : CaseGroup.py
@Desc    :
"""
from flask import jsonify
from lin import login_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.CaseGroup import CaseGroup
from app.validators.CaseForm import CaseGroupForm, CaseGroupSearchForm

case_croup_api = Redprint('caseGroup')

@case_croup_api.route('/<gid>', methods=['GET'])
# @login_required
def get_group(gid):
    group = CaseGroup.get_detail(gid)
    return jsonify(group)

@case_croup_api.route('', methods=['POST'])
# @login_required
def create_group():
    form = CaseGroupForm().validate_for_api()
    CaseGroup.new_group(form)
    return Success(msg='新建分组成功')

@case_croup_api.route('', methods=['GET'])
# @login_required
def get_groups():
    groups = CaseGroup.get_all()
    return jsonify(groups)

@case_croup_api.route('/search', methods=['GET'])
# @login_required
def search():
    form = CaseGroupSearchForm().validate_for_api()
    groups = CaseGroup.search_by_keywords(form.name.data)
    return jsonify(groups)

@case_croup_api.route('/<gid>', methods=['PUT'])
# @login_required
def update_group(gid):
    form = CaseGroupForm().validate_for_api()
    CaseGroup.edit_group(gid, form)
    return Success(msg='更新分组成功')