""" 
@Time    : 2020/3/14 10:13
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : CaseGroup.py
@Desc    :
"""
from flask import jsonify
from lin import login_required
from lin.redprint import Redprint

from app.models.CaseGroup import CaseGroup

case_croup_api = Redprint('caseGroup')

@case_croup_api.route('', methods=['GET'])
@login_required
def get_groups():
    groups = CaseGroup.get_all()
    return jsonify(groups)