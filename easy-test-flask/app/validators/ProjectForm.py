"""
@Time    : 2020/4/11 14:57
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : ProjectForm.py
@Desc    :
"""
from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField, DateTimeField
from wtforms.validators import DataRequired, length, Optional


class ProjectForm(Form):
    # 工程 name
    name = StringField(length(max=20, message='描述文字长度应小于20个字'),
                       validators=[DataRequired(message='请输入工程名称')])

    # 服务地址
    server = StringField(length(max=60, message='描述文字长度应小于60个字'),
                         validators=[DataRequired(message='请输入服务地址')])

    # 公共请求头
    header = StringField(length(max=500, message='header长度应小于500个字'),
                         validators=[Optional()])

    # 工程描述
    info = StringField(length(max=50, message='描述文字长度应小于50个字'),
                       validators=[Optional()])

    # 工程类型
    type = IntegerField(default=1)

    users = FieldList(IntegerField(validators=[Optional()]))
