import json

from flask import request
from lin.redprint import Redprint

from app.libs.enums import CaseMethodEnum
from app.libs.error_code import MethodMockException
from app.libs.init import mongo

mock_api = Redprint('mock')


@mock_api.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def mock(path):
    methodData = {
        'GET': '1',
        'POST': '2',
        'PUT': '3',
        'DELETE': '4',
    }
    mocks = mongo.db.mock.find(
        {
            'url': '/mock/' + path,
            'method': methodData[request.method],
            'delete_time': None
        },
        {"_id": 0}).sort([('_id', -1)])

    mocks = list(mocks)
    if not mocks:
        raise MethodMockException()

    response_body = json.loads(mocks[0]['response_body']) if mocks[0]['response_body'] else ''
    status_code = mocks[0]['status_code']
    response_header = json.loads(mocks[0]['response_header']) if mocks[0]['response_header'] else ''

    return response_body, status_code, response_header
