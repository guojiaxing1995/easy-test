"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

# 安全性配置
from apscheduler.jobstores.mongodb import MongoDBJobStore

from app.config.setting import BaseConfig


class DevelopmentSecure(BaseConfig):
    """
    开发环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@ip:3306/easy-test'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x85\x87\x96\xb0A\xc68\xf9\xecJJU\x12\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*6'

    MONGO_URI = 'mongodb://root:root@ip:27017/easyTest?authSource=admin'

    CELERY_BROKER_URL = 'amqp://admin:admin@ip:8083/my_vhost'

    # scheduler
    SCHEDULER_JOBSTORES = {
        'default': MongoDBJobStore(host='ip', port=27017, username='root', password='root')
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,  # 累计的 任务是否执行。True不执行，False,执行
        'max_instances': 30,  # 同一个任务在线程池中最多跑的实例数
        'misfire_grace_time': 600  # 超过用户设定的时间范围外，该任务依旧执行的时间(单位时间s)
    }

    SCHEDULER_API_ENABLED = True

    # mail
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # mock server
    MOCK_SERVER = 'http://127.0.0.1:5000'

    API_SERVER = 'http://127.0.0.1:5000'

    SITE_DOMAIN = 'http://127.0.0.1:5000'


class ProductionSecure(BaseConfig):
    """
    生产环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@mysql:3306/easy-test'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x85\x87\x96\xb0A\xc68\xf9\xecJJU\x12\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*6'

    MONGO_URI = 'mongodb://root:mongo2020@mongo:27017/easyTest?authSource=admin'

    CELERY_BROKER_URL = 'amqp://admin:ftlb2000@rabbitmq:5672/my_vhost'

    # scheduler
    SCHEDULER_JOBSTORES = {
        'default': MongoDBJobStore(host='mongo', port=27017, username='root', password='mongo2020')
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': True,  # 累计的 任务是否执行。True不执行，False,执行
        'max_instances': 30,  # 同一个任务在线程池中最多跑的实例数
        'misfire_grace_time': 600  # 超过用户设定的时间范围外，该任务依旧执行的时间(单位时间s)
    }

    SCHEDULER_API_ENABLED = True

    # mail
    MAIL_SERVER = 'smtp.sina.cn'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ''
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    # mock server
    MOCK_SERVER = 'http://api:5000'

    API_SERVER = 'http://api:5000'

    SITE_DOMAIN = ''
