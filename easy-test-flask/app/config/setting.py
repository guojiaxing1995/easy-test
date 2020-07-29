"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from datetime import timedelta


class BaseConfig(object):
    """
    基础配置
    """
    # 分页配置
    COUNT_DEFAULT = 10
    PAGE_DEFAULT = 0

    # 屏蔽 sql alchemy 的 FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """
    开发环境普通配置
    """
    DEBUG = True

    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 插件模块暂时没有开启，以下配置可忽略
    # plugin config写在字典里面
    PLUGIN_PATH = {
        'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
        'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete',
                'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com',
                'bucket_name': 'not complete', 'upload_folder': 'app',
                'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,  # 累计的 任务是否执行。True不执行，False,执行
        'max_instances': 30,  # 同一个任务在线程池中最多跑的实例数
        'misfire_grace_time': 600  # 超过用户设定的时间范围外，该任务依旧执行的时间(单位时间s)
    }

    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

    SCHEDULER_API_ENABLED = True


class ProductionConfig(BaseConfig):
    """
    生产环境普通配置
    """
    DEBUG = False

    # 令牌配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    # 插件模块暂时没有开启，以下配置可忽略
    # plugin config写在字典里面
    PLUGIN_PATH = {
        'poem': {'path': 'app.plugins.poem', 'enable': True, 'version': '0.0.1', 'limit': 20},
        'oss': {'path': 'app.plugins.oss', 'enable': True, 'version': '0.0.1', 'access_key_id': 'not complete',
                'access_key_secret': 'not complete', 'endpoint': 'http://oss-cn-shenzhen.aliyuncs.com',
                'bucket_name': 'not complete', 'upload_folder': 'app',
                'allowed_extensions': ['jpg', 'gif', 'png', 'bmp']}
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,  # 累计的 任务是否执行。True不执行，False,执行
        'max_instances': 30,  # 同一个任务在线程池中最多跑的实例数
        'misfire_grace_time': 600  # 超过用户设定的时间范围外，该任务依旧执行的时间(单位时间s)
    }

    # Etc/UTC
    SCHEDULER_TIMEZONE = 'Asia/Shanghai'

    SCHEDULER_API_ENABLED = True
