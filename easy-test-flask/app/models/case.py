"""
@Time    : 2020/3/25 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 测试用例模型
"""
from datetime import datetime
import json
import re
import requests
from flask import current_app
from flask_jwt_extended import current_user, get_current_user
from lin.exception import ParameterException, AuthFailed
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger
from lin.db import db
from app.libs.enums import CaseMethodEnum, CaseSubmitEnum, CaseDealEnum, CaseTypeEnum, CaseAssertEnum, UserAuthEnum
from app.libs.utils import paging
from sqlalchemy import text

from app.models.UserAuth import UserAuth


class Case(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用例id')
    name = Column(String(20), nullable=False, comment='用例名称 组内唯一不可重复')
    info = Column(String(50), comment='用例描述')
    url = Column(String(500), comment='请求地址')
    _method = Column('method', SmallInteger, nullable=False,
                     comment='请求方法 ;  1 -> get |  2 -> post |  3 -> put |  4-> delete')
    _submit = Column('submit', SmallInteger, nullable=False, comment='提交方法 ;  1 -> json提交 |  2 -> 表单提交')
    header = Column(String(500), comment='请求头')
    data = Column(String(500), comment='请求体')
    _deal = Column('deal', SmallInteger, nullable=False,
                   comment='后置处理方法 ;  1 -> 不做处理 |  2 -> 默认处理 |  3 -> 指定key获取数据 |  4-> 正则表达')
    condition = Column(String(50), comment='后置处理方法的条件语句，在后置处理方法为指定key或正则表达时为必填')
    expect_result = Column(String(500), comment='预期结果')
    _assertion = Column('assertion', SmallInteger, nullable=False,
                        comment='断言类型 ;  1 -> key value 等于 |  2 -> key value 不等于 |  3 -> 包含|  4-> 不包含|  4-> http返回码200')
    _type = Column('type', SmallInteger, nullable=False, comment='用例类型 ;  1 -> 接口自动化 |  2 -> UI自动化')
    case_group = Column(Integer, nullable=False, comment='用例分组id')
    create_user = Column(Integer, nullable=False, comment='用例创建人')
    update_user = Column(Integer, nullable=False, comment='用例修改人')

    def __init__(self, case_group, name=None, info=None, url=None, method=1, submit=1, header=None, data=None, deal=1,
                 condition=None, expect_result=None, assertion=1, case_type=1):
        super().__init__()
        self.name = name
        self.info = info
        self.url = url
        self.method = CaseMethodEnum(method)
        self.submit = CaseSubmitEnum(submit)
        self.header = header
        self.data = data
        self.deal = CaseDealEnum(deal)
        self.condition = condition
        self.expect_result = expect_result
        self.assertion = CaseAssertEnum(assertion)
        self.type = CaseTypeEnum(case_type)
        self.case_group = case_group
        self.create_user = get_current_user().id if get_current_user() else None
        self.update_user = get_current_user().id if get_current_user() else None

    @property
    def method(self):
        return CaseMethodEnum(self._method).value

    @method.setter
    def method(self, methodEnum):
        self._method = methodEnum.value

    @property
    def submit(self):
        return CaseSubmitEnum(self._submit).value

    @submit.setter
    def submit(self, submitEnum):
        self._submit = submitEnum.value

    @property
    def deal(self):
        return CaseDealEnum(self._deal).value

    @deal.setter
    def deal(self, dealEnum):
        self._deal = dealEnum.value

    @property
    def assertion(self):
        return CaseAssertEnum(self._assertion).value

    @assertion.setter
    def assertion(self, assertEnum):
        self._assertion = assertEnum.value

    @property
    def type(self):
        return CaseTypeEnum(self._type).value

    @type.setter
    def type(self, typeEnum):
        self._type = typeEnum.value

    #    新增用例
    def new_case(self):
        if Case.query.filter_by(name=self.name, case_group=self.case_group, delete_time=None).first():
            raise ParameterException(msg='当前组已存在同名用例，请更改用例名称')
        db.session.add(self)
        db.session.commit()

    def edit_case(self, name, info, url, method, submit, header, data, deal, condition, expect_result, assertion,
                  type):
        if self.name != name:
            if Case.query.filter_by(name=name, case_group=self.case_group, delete_time=None).first():
                raise ParameterException(msg='当前组已存在同名用例，请更改用例名称')
        self.name = name
        self.info = info
        self.url = url
        self.method = CaseMethodEnum(method)
        self.submit = CaseSubmitEnum(submit)
        self.header = header
        self.data = data
        self.deal = CaseDealEnum(deal)
        self.condition = condition
        self.expect_result = expect_result
        self.assertion = CaseAssertEnum(assertion)
        self.type = CaseTypeEnum(type)
        self.update_user = get_current_user().id
        self.update_user = 1
        db.session.commit()

    def remove_case(self):
        auth = UserAuth.query.filter_by(user_id=current_user.id, auth_id=self.case_group,
                                        _type=UserAuthEnum.GROUP.value).first()
        if auth or current_user.id == 1:
            self.delete_time = datetime.now()
            self.update_user = get_current_user().id
            self.update_user = 1
            db.session.commit()
        else:
            raise AuthFailed(msg='无删除此用例的权限')

    @classmethod
    def search_case(cls, name, url, case_group, start, end, id, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        auths = UserAuth.query.filter_by(user_id=current_user.id, _type=UserAuthEnum.GROUP.value).all()
        gids = [auth.auth_id for auth in auths]
        from app.models.CaseGroup import CaseGroup
        results = cls.query.join(CaseGroup, CaseGroup.id == cls.case_group).filter(
            cls.id == id if id else '',
            cls.case_group == case_group if case_group else '',
            cls.name.like(f'%{name}%') if name is not None else '',
            cls.url.like(f'%{url}%') if url is not None else '',
            cls._update_time.between(start, end) if start and end else '',
            cls.case_group.in_(gids) if current_user.id != 1 else '',
            cls.delete_time == None,
        ).with_entities(
            cls.id,
            cls.name,
            cls.info,
            cls.url,
            cls._method.label('method'),
            cls._submit.label('submit'),
            cls.header,
            cls.data,
            cls._deal.label('deal'),
            cls.condition,
            cls._type.label('type'),
            cls.expect_result.label('expect_result'),
            cls._assertion.label('assertion'),
            cls.case_group.label('case_group'),
            CaseGroup.name.label('group_name')
        ).order_by(
            text('Case.update_time desc')
        ).paginate(page, count)

        items = [dict(zip(result.keys(), result)) for result in results.items]
        results.items = items
        data = paging(results)
        return data

    # 通过用例分组查询用例
    @classmethod
    def cases_by_group(cls, group):
        cases = cls.query.filter(
            cls.case_group == group if group else '',
            cls.delete_time == None,
        ).order_by(
            text('update_time desc')
        ).all()
        return cases

    # 字符串转字典
    def str_to_dict(self):
        self.data = json.loads(self.data) if self.data else self.data
        self.header = json.loads(self.header) if self.header else self.header

    def get_request(self):
        res = requests.get(url=self.url, params=self.data, headers=self.header)
        return res

    def post_request(self):
        if self.submit == CaseSubmitEnum.JSON.value:
            res = requests.post(url=self.url, json=self.data, headers=self.header)
        elif self.submit == CaseSubmitEnum.FORM.value:
            res = requests.post(url=self.url, data=self.data, headers=self.header)
        return res

    def put_request(self):
        if self.submit == CaseSubmitEnum.JSON.value:
            res = requests.put(url=self.url, json=self.data, headers=self.header)
        elif self.submit == CaseSubmitEnum.FORM.value:
            res = requests.put(url=self.url, data=self.data, headers=self.header)
        return res

    def delete_request(self):
        if self.submit == CaseSubmitEnum.JSON.value:
            res = requests.delete(url=self.url, json=self.data, headers=self.header)
        elif self.submit == CaseSubmitEnum.FORM.value:
            res = requests.delete(url=self.url, data=self.data, headers=self.header)
        return res

    def method_request(self):
        res = None
        if self.method == CaseMethodEnum.GET.value:
            res = self.get_request()
        elif self.method == CaseMethodEnum.POST.value:
            res = self.post_request()
        elif self.method == CaseMethodEnum.PUT.value:
            res = self.put_request()
        elif self.method == CaseMethodEnum.DELETE.value:
            res = self.delete_request()

        return res

    # 用例调试
    def case_debug(self):
        self.str_to_dict()
        try:
            res = self.method_request()
        except Exception:
            raise ParameterException(msg='参数错误')
        status_code = res.status_code
        try:
            body = res.json()
        except Exception:
            body = res.text

        result = {
            'statusCode': status_code,
            'body': body,
            'headers': res.headers,
            'cookies': res.cookies,
            'encoding': res.encoding,
            'totalSeconds': res.elapsed.total_seconds()
        }
        return result
