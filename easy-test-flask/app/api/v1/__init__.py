"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1 import book, CaseGroup, case, project


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    book.book_api.register(bp_v1)
    CaseGroup.case_group_api.register(bp_v1)
    case.case_api.register(bp_v1)
    project.project_api.register(bp_v1)
    return bp_v1
