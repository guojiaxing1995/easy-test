"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

# 安全性配置
from app.config.setting import BaseConfig


class DevelopmentSecure(BaseConfig):
    """
    开发环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:3306/easy-test'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x85\x87\x96\xb0A\xc68\xf9\xecJJU\x12\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*6'


class ProductionSecure(BaseConfig):
    """
    生产环境安全性配置
    """
    SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@127.0.0.1:3306/easy-test'

    SQLALCHEMY_ECHO = False

    SECRET_KEY = '\x88W\xf09\x91\x07\x98\x85\x87\x96\xb0A\xc68\xf9\xecJJU\x12\xc5V\xbe\x8b\xef\xd7\xd8\xd3\xe6\x95*6'
