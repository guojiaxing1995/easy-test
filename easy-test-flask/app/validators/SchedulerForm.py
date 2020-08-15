from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField, BooleanField, FormField, Field
from wtforms.validators import DataRequired, Optional, length


class SchedulerForm(Form):
    # 工程 id
    project = IntegerField(validators=[DataRequired(message='请输入工程id')])
    user = IntegerField(validators=[DataRequired(message='请输入维护人员')])
    sendEmail = BooleanField(validators=[Optional()])
    copyPerson = StringField(length(max=50, message='抄送人需小于50字符'), validators=[Optional()])
    cron = StringField(length(max=30, message='cron表达式需小于30字符'), validators=[DataRequired(message='请输入cron表达式')])
    # 邮件发送策略
    emailStrategy = IntegerField(default=1)


class SchedulerEditForm(Form):
    user = IntegerField(validators=[DataRequired(message='请输入维护人员')])
    sendEmail = BooleanField(validators=[Optional()])
    copyPerson = StringField(length(max=50, message='抄送人需小于50字符'), validators=[Optional()])
    cron = StringField(length(max=30, message='cron表达式需小于30字符'), validators=[DataRequired(message='请输入cron表达式')])
    # 邮件发送策略
    emailStrategy = IntegerField(default=1)


class SchedulerSearchForm(Form):
    page = IntegerField(default=1)
    count = IntegerField(default=10)
    project = IntegerField()
    user = IntegerField()


class SchedulerOperateForm(Form):
    schedulerId = StringField(validators=[DataRequired(message='不许为空')])
