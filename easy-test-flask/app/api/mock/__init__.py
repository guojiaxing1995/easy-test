from flask import Blueprint
from app.api.mock import mock


def create_mock():
    bp_mock = Blueprint('mock', __name__)
    mock.mock_api.register(bp_mock)

    return bp_mock
