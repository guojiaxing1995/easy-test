import time

from lin.forms import Form
from wtforms import StringField, IntegerField, DateTimeField, Field
from wtforms.validators import DataRequired, length, Optional


class TaskSearchForm(Form):
    project = IntegerField(validators=[Optional()])
    no = StringField(validators=[Optional()])
    user = IntegerField(validators=[Optional()])
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
