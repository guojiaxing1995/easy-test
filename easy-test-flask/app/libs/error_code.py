"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from lin.exception import APIException


class BookNotFound(APIException):
    code = 404  # http状态码
    msg = '没有找到相关图书'  # 异常信息
    error_code = 80010  # 约定的异常码


class RefreshException(APIException):
    code = 401
    msg = 'refresh token 获取失败'
    error_code = 10100


class CaseGroupDeleteException(APIException):
    code = 401
    msg = '删除测试用例分组失败'
    error_code = 91001


class ProjectConfigException(APIException):
    code = 403
    msg = '保存配置异常'
    error_code = 92001


class ConfigNotFound(APIException):
    code = 404
    msg = '配置不存在'
    error_code = 92002


class ProjectNotFound(APIException):
    code = 404
    msg = '工程不存在'
    error_code = 92003


class CaseRemoveException(APIException):
    code = 403
    msg = '用例删除失败'
    error_code = 93001


class CaseUploadExcelException(APIException):
    code = 400
    msg = 'excel用例数据异常'
    error_code = 93002


class CaseDownloadException(APIException):
    code = 400
    msg = '用例导出数据异常'
    error_code = 93003


class RecordRemoveException(APIException):
    code = 403
    msg = '运行记录删除失败'
    error_code = 94001


class AddMockException(APIException):
    code = 400
    msg = '新增mock数据失败'
    error_code = 95001


class EditMockException(APIException):
    code = 400
    msg = '编辑mock数据失败'
    error_code = 95002


class MethodMockException(APIException):
    code = 405
    msg = '请求方法错误'
    error_code = 95003
