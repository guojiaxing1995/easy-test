""" 
@Time    : 2020/2/23 17:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : user.py.py
@Desc    :
"""
from lin.core import User as _User
from sqlalchemy import Column, String


class User(_User):
    # 扩展user
    phone = Column(String(20), unique=True, comment='手机号')
    openid = Column(String(255), unique=True, comment='微信openid')
