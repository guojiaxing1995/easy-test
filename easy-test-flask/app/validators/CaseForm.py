""" 
@Time    : 2020/3/14 11:00
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : CaseForm.py
@Desc    :
"""
from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired, length, Optional

class CaseGroupForm(Form):
    # 分组name
    name = StringField(length(max=20, message='描述文字长度应小于20个字'),
                        validators=[DataRequired(message='请输入分组名称')])
    # 非必须
    info = StringField(length(max=50, message='描述文字长度应小于50个字'),
                        validators=[Optional()])

    users = FieldList(IntegerField(validators=[Optional()]))

class CaseGroupSearchForm(Form):
    name = StringField(validators=[DataRequired(message='请输入分组名称')])