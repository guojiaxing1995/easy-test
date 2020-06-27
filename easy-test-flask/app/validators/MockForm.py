from lin.forms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Optional


class MockForm(Form):
    url = StringField(validators=[DataRequired(message='请输入url')])
    method = IntegerField(default=1)
    requestHeader = StringField(validators=[Optional()])
    requestBody = StringField(validators=[Optional()])
    responseHeader = StringField(validators=[Optional()])
    responseBody = StringField(validators=[Optional()])
    statusCode = IntegerField(default=200)
    msg = StringField(validators=[Optional()])


class MockSearchForm(Form):
    url = StringField()
    mid = IntegerField()
