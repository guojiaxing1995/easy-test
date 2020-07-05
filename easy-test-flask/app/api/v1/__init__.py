"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1 import book, CaseGroup, case, project, task, scheduler, user, mock, overview


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    book.book_api.register(bp_v1)
    CaseGroup.case_group_api.register(bp_v1)
    case.case_api.register(bp_v1)
    project.project_api.register(bp_v1)
    task.task_api.register(bp_v1)
    scheduler.scheduler_api.register(bp_v1)
    user.user_api.register(bp_v1)
    mock.mock_api.register(bp_v1)
    overview.overview_api.register(bp_v1)
    return bp_v1
