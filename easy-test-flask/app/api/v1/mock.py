from flask import jsonify, current_app
from lin import route_meta, group_required
from lin.exception import Success
from lin.redprint import Redprint

from app.models.mock import Mock
from app.validators.MockForm import MockForm, MockSearchForm

mock_api = Redprint('mock')


@mock_api.route('', methods=['POST'])
@route_meta('mock', module='mock管理')
@group_required
def add_mock():
    form = MockForm().validate_for_api()
    mock = Mock(form.method.data, form.url.data, form.requestHeader.data, form.requestBody.data,
                form.responseHeader.data, form.responseBody.data, form.statusCode.data, form.msg.data)
    mock.new_mock()

    return Success(msg='新增mock成功')


@mock_api.route('/<mid>', methods=['PUT'])
@route_meta('mock', module='mock管理')
@group_required
def edit_mock(mid):
    form = MockForm().validate_for_api()
    mock = Mock(form.method.data, form.url.data, form.requestHeader.data, form.requestBody.data,
                form.responseHeader.data, form.responseBody.data, form.statusCode.data, form.msg.data)
    mock.mid = mid
    mock.edit_mock()

    return Success(msg='修改mock成功')


@mock_api.route('/<mid>', methods=['DELETE'])
@route_meta('mock', module='mock管理')
@group_required
def delete_mock(mid):
    mock = Mock()
    mock.mid = mid
    mock.delete_mock()

    return Success(msg='删除mock成功')


@mock_api.route('', methods=['GET'])
@route_meta('mock', module='mock管理')
@group_required
def search_mock():
    form = MockSearchForm().validate_for_api()
    mocks = Mock.search_mock(form.mid.data, form.url.data)

    return jsonify(mocks)


@mock_api.route('/server', methods=['GET'])
@route_meta('mock', module='mock管理')
@group_required
def mock_server():
    # 获取mock server
    result = {
        'server': current_app.config.get('MOCK_SERVER')
    }

    return result
