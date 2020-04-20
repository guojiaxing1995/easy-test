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
