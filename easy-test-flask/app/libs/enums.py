""" 
@Time    : 2020/3/15 9:52
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : enums.py
@Desc    : 枚举类
"""
from enum import Enum, unique


@unique
class UserAuthEnum(Enum):
    '''用户权限枚举类'''
    GROUP = 1
    project = 2


