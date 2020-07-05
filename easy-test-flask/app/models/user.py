""" 
@Time    : 2020/2/23 17:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : user.py.py
@Desc    :
"""
from lin import db
from lin.core import User as _User
from sqlalchemy import Column, String


class User(_User):
    # 扩展user
    phone = Column(String(20), unique=True, comment='手机号')
    openid = Column(String(255), unique=True, comment='微信openid')

    @classmethod
    def execute_top(cls):
        # 执行测试次数top3

        execute_top = db.session.execute("SELECT lin_user.username,count( * ) AS count FROM `task`,`lin_user` WHERE "
                                         "lin_user.id = task.create_user AND task.delete_time IS NULL AND "
                                         "create_user > 0 GROUP BY create_user ORDER BY count( * ) DESC LIMIT 3")

        return list(execute_top)

