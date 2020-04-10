"""
@Time    : 2020/3/14 11:00
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : CaseForm.py
@Desc    :
"""
import time

from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField, DateTimeField
from wtforms.validators import DataRequired, length, Optional

class CaseGroupForm(Form):
    # 分组name
    name = StringField(length(max=20, message='描述文字长度应小于20个字'),
                        validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(length(max=50, message='描述文字长度应小于50个字'),
                        validators=[Optional()])

    users = FieldList(IntegerField(validators=[Optional()]))

class UserGroupAuthForm(Form):
    # 权限组id 可以不传，编辑传值，新增不传
    authId = IntegerField(validators=[Optional()])
    # 权限类型 对应权限枚举类
    authType = IntegerField(validators=[Optional()])

class CaseForm(Form):
    name = StringField(length(max=20, message='用例名称应小于20个字'),
                        validators=[DataRequired(message='请输入用例名称')])
    info = StringField(length(max=50, message='描述文字长度应小于50个字'),
                        validators=[Optional()])
    url = StringField(length(max=500, message='url长度应小于500个字'),
                        validators=[DataRequired(message='请输入url')])
    method = IntegerField(default=1)
    submit = IntegerField(default=1)
    header = StringField(length(max=500, message='header长度应小于500个字'),
                        validators=[Optional()])
    data = StringField(length(max=500, message='data长度应小于500个字'),
                        validators=[Optional()])
    deal = IntegerField(default=1)
    condition = StringField(length(max=50, message='处理语句长度应小于50个字'),
                        validators=[Optional()])
    expectResult = StringField(length(max=500, message='预期结果长度应小于500个字'),
                        validators=[Optional()])
    caseAssert = IntegerField(default=1)
    type = IntegerField(default=1)
    caseGroup = IntegerField(validators=[Optional()])

class CaseSearchForm(Form):
    id = IntegerField(validators=[Optional()])
    name = StringField(validators=[Optional()])
    url = StringField(validators=[Optional()])
    caseGroup = IntegerField(validators=[Optional()])
    page = IntegerField(validators=[Optional()])
    count = IntegerField(validators=[Optional()])
    start = DateTimeField(validators=[])
    end = DateTimeField(validators=[])

    def validate_start(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e

    def validate_end(self, value):
        if value.data:
            try:
                _ = time.strptime(value.data, '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                raise e

class EnumTypeForm(Form):
    type = StringField(validators=[DataRequired(message='请输入类型值')])

#用例调试
class CaseDebugForm(Form):
    url = StringField(length(max=500, message='url长度应小于500个字'),
                      validators=[DataRequired(message='请输入url')])
    method = IntegerField(default=1)
    header = StringField(length(max=500, message='header长度应小于500个字'),
                         validators=[Optional()])
    data = StringField(length(max=500, message='data长度应小于500个字'),
                       validators=[Optional()])
    submit = IntegerField(default=1)
