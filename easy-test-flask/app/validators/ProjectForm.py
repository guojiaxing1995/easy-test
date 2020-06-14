"""
@Time    : 2020/4/11 14:57
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : ProjectForm.py
@Desc    :
"""
from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField, BooleanField, FormField, Field
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

    # 授权人员
    users = FieldList(IntegerField(validators=[Optional()]))

    # 维护人员
    user = IntegerField(validators=[DataRequired(message='请输入维护人员')])

    # 是否发送邮件
    sendEmail = BooleanField(validators=[Optional()])

    # 邮件抄送人
    copyPerson = StringField(length(max=50, message='抄送人需小于50字符'), validators=[Optional()])


class ProjectSearchForm(Form):
    # 工程 name
    name = StringField(validators=[Optional()])


class ProjectPaginateForm(Form):
    # 工程 name
    name = StringField(validators=[Optional()])
    page = IntegerField(default=1)
    count = IntegerField(default=10)


class ProjectConfigForm(Form):
    projectId = IntegerField(validators=[DataRequired(message='请输入工程id')])
    # 配置 [[configId, caseId, isRun, order], []]
    configs = FieldList(Field(validators=[Optional()]))


class CopyConfigForm(Form):
    id = IntegerField()
    projectId = IntegerField(validators=[DataRequired(message='请输入工程id')])
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
    expect = StringField(length(max=500, message='预期结果长度应小于500个字'),
                               validators=[Optional()])
    assertion = IntegerField(default=1)
