import time

from lin.forms import Form
from wtforms import StringField, FieldList, IntegerField, DateTimeField, Field
from wtforms.validators import DataRequired, length, Optional


class MineSearchForm(Form):
    uid = IntegerField()
    # project | case | scheduler  name
    name = StringField(length(max=20, message='描述文字长度应小于30个字'))
    page = IntegerField(default=1)
    count = IntegerField(default=10)
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
