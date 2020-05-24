"""
@Time    : 2020/3/25 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 测试用例模型
"""
import math
import time
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

from app.libs.case_log import log
from app.libs.deal import deal_default, get_target_value
from app.libs.enums import CaseMethodEnum, CaseSubmitEnum, CaseDealEnum, CaseTypeEnum, CaseAssertEnum, UserAuthEnum
from app.libs.error_code import CaseRemoveException
from app.libs.init import mongo
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
    expect = Column(String(500), comment='预期结果')
    _assertion = Column('assertion', SmallInteger, nullable=False,
                        comment='断言类型 ;  1 -> key value 等于 |  2 -> key value 不等于 |  3 -> 包含|  4-> 不包含|  4-> http返回码200')
    _type = Column('type', SmallInteger, nullable=False, comment='用例类型 ;  1 -> 接口自动化 |  2 -> UI自动化')
    case_group = Column(Integer, nullable=False, comment='用例分组id')
    create_user = Column(Integer, nullable=False, comment='用例创建人')
    update_user = Column(Integer, nullable=False, comment='用例修改人')

    def __init__(self, case_group, name=None, info=None, url=None, method=1, submit=1, header=None, data=None, deal=1,
                 condition=None, expect=None, assertion=1, case_type=1):
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
        self.expect = expect
        self.assertion = CaseAssertEnum(assertion)
        self.type = CaseTypeEnum(case_type)
        self.case_group = case_group
        self.create_user = get_current_user().id if get_current_user() else None
        self.update_user = get_current_user().id if get_current_user() else None
        self.actual_result = False
        self.reason = None
        self.result = {}

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

    def edit_case(self, name, info, url, method, submit, header, data, deal, condition, expect, assertion,
                  type):
        if self.name != name:
            if Case.query.filter_by(name=name, case_group=self.case_group, delete_time=None).first():
                raise ParameterException(msg='当前组已存在同名用例，请更改用例名称')
        # 用例名称暂时不允许修改
        # self.name = name
        self.info = info
        self.url = url
        self.method = CaseMethodEnum(method)
        self.submit = CaseSubmitEnum(submit)
        self.header = header
        self.data = data
        self.deal = CaseDealEnum(deal)
        self.condition = condition
        self.expect = expect
        self.assertion = CaseAssertEnum(assertion)
        self.type = CaseTypeEnum(type)
        self.update_user = get_current_user().id
        db.session.commit()

    def remove_case(self):
        from app.models.ConfigRelation import ConfigRelation
        copy_config = ConfigRelation.query.filter_by(case_id=self.id).first()
        if copy_config:
            raise CaseRemoveException(msg='用例已被工程关联，无法删除')
        auth = UserAuth.query.filter_by(user_id=current_user.id, auth_id=self.case_group,
                                        _type=UserAuthEnum.GROUP.value).first()
        if auth or current_user.is_admin:
            self.delete_time = datetime.now()
            self.update_user = get_current_user().id
            self.update_user = 1
            db.session.commit()
        else:
            raise AuthFailed(msg='无删除此用例的权限')

    @classmethod
    def search_case(cls, name, url, case_group, start, end, cid, method, deal, page=None, count=None):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        auths = UserAuth.query.filter_by(user_id=current_user.id, _type=UserAuthEnum.GROUP.value).all()
        gids = [auth.auth_id for auth in auths]
        from app.models.CaseGroup import CaseGroup
        results = cls.query.join(CaseGroup, CaseGroup.id == cls.case_group).filter(
            cls.id == cid if cid else '',
            cls._method == method if method else '',
            cls._deal == deal if deal else '',
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
            cls.expect.label('expect'),
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

    # 执行一条用例
    def execute_one(self, project, task, create_user):
        try:
            self.stitch_url(project.server)
            self.replace_header(project.header)
            self.str_to_dict()
            self.var_substitution(project.var_dick)
            res = self.method_request()
            self.return_deal(project.var_dick, res.json())
            self.get_result(res)
            self.assert_result()
            self.update_task_result(task)
        except Exception as e:
            self.actual_result = False
            self.reason = str(e)
            current_app.logger.debug(self.reason)

        # 用例执行日志插入mongoDB数据库
        case_log = log(self, project, task, create_user)
        mongo.db.easy.insert(case_log)
        # 向客户端广播用例日志
        res = requests.get(url='http://127.0.0.1:5000/v1/task/log/' + str(task.task_no))
        current_app.logger.debug(res.text)

    # 拼接请求地址
    def stitch_url(self, server):
        self.url = server + self.url
        if 'http' not in self.url:
            self.url = 'http://' + self.url

    # 找到${var} 替换变量的值
    # re.search(r'\${(.*)\}','/v1/${job}o').group(0)  '${job}' |  re.search(r'\${(.*)\}','/v1/${job}o').group(1)  'job'
    def var_substitution(self, var_dick):
        # url 处理
        url_var = re.search(r'\${(.*)\}', self.url)
        if url_var:
            var = var_dick[url_var.group(1)]
            self.url = self.url.replace(url_var.group(0), str(var))
        # header 处理
        if self.header:
            for key, value in self.header.items():
                if type(value) == str:
                    header_var = re.search(r'\${(.*)\}', value)
                    if header_var:
                        self.header[key] = var_dick[header_var.group(1)]
        # data 处理
        if self.data:
            for key, value in self.data.items():
                if type(value) == str:
                    data_var = re.search(r'\${(.*)\}', value)
                    if data_var:
                        self.data[key] = var_dick[data_var.group(1)]

    # 后置处理
    def return_deal(self, var_dick, interface_return):
        if self.deal == CaseDealEnum.DEFAULT.value:
            var_dick = deal_default(var_dick, interface_return)
        # condition 'target_key,new_key  target_key,new_key'
        elif self.deal == CaseDealEnum.JSON.value:
            items = self.condition.split()
            for item in items:
                # 目标key
                target_key = item.split(',')[0]
                # 新key
                new_key = item.split(',')[1]
                var_dick = deal_default(var_dick, interface_return, target_key, new_key)
        # condition  'pattern,key  pattern,key'
        elif self.deal == CaseDealEnum.REGULAR.value:
            items = self.condition.split()
            for item in items:
                # 正则表达式
                pattern = item.split(',')[0]
                # 新key
                key = item.split(',')[1]
                value = re.findall(pattern, json.dumps(interface_return, ensure_ascii=False))
                if value:
                    var_dick[key] = value[0]
        current_app.logger.debug(json.dumps(var_dick))
        return var_dick

    # 如果用例header不存在则将工程header赋值给用例
    def replace_header(self, header):
        self.header = header if not self.header else self.header

    # 更新任务表成功数和失败数
    def update_task_result(self, task):
        if self.actual_result:
            success = task.success + 1
            task.update_result(success)
        else:
            fail = task.fail + 1
            task.update_result(fail=fail)

    # 判断用例执行结果是否通过
    def assert_result(self):
        if self.assertion == CaseAssertEnum.EQUAL.value:
            # 目标key
            target_key = self.expect.split(',')[0]
            # 比较value
            value = self.expect.split(',')[1]
            target_value = get_target_value(self.result['body'], target_key)
            if target_value != value:
                self.actual_result = False
                self.reason = '实际结果值与预期结果不相等'
            else:
                self.actual_result = True
        elif self.assertion == CaseAssertEnum.NOTEQUAL.value:
            # 目标key
            target_key = self.expect.split(',')[0]
            # 比较value
            value = self.expect.split(',')[1]
            target_value = get_target_value(self.result['body'], target_key)
            if target_value == value:
                self.actual_result = False
                self.reason = '实际结果值与预期结果相等'
            else:
                self.actual_result = True
        elif self.assertion == CaseAssertEnum.IN.value:
            if self.expect in self.result['text']:
                self.actual_result = True
            else:
                self.actual_result = False
                self.reason = '实际结果不在预期结果中'
        elif self.assertion == CaseAssertEnum.NOTIN.value:
            if self.expect not in self.result['text']:
                self.actual_result = True
            else:
                self.actual_result = False
                self.reason = '实际结果在预期结果中'
        elif self.assertion == CaseAssertEnum.SUCCESS.value:
            if self.result['statusCode'] == 200:
                self.actual_result = True
            else:
                self.actual_result = False
                self.reason = 'HTTP状态码不是200'
        current_app.logger.debug(self.id)
        current_app.logger.debug(self.actual_result)
        current_app.logger.debug(self.result['body'])

    # 字符串转字典
    def str_to_dict(self):
        self.data = json.loads(self.data) if self.data else self.data
        self.header = json.loads(self.header) if self.header else self.header

    def get_request(self):
        res = requests.get(url=self.url, params=self.data, headers=self.header)
        return res

    def post_request(self):
        res = None
        if self.submit == CaseSubmitEnum.JSON.value:
            res = requests.post(url=self.url, json=self.data, headers=self.header)
        elif self.submit == CaseSubmitEnum.FORM.value:
            res = requests.post(url=self.url, data=self.data, headers=self.header)
        return res

    def put_request(self):
        res = None
        if self.submit == CaseSubmitEnum.JSON.value:
            res = requests.put(url=self.url, json=self.data, headers=self.header)
        elif self.submit == CaseSubmitEnum.FORM.value:
            res = requests.put(url=self.url, data=self.data, headers=self.header)
        return res

    def delete_request(self):
        res = None
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

    # 获取结果对象
    def get_result(self, res):
        status_code = res.status_code
        try:
            body = res.json()
        except Exception:
            body = res.text

        result = {
            'statusCode': status_code,
            'body': body,
            'text': res.text,
            'headers': res.headers,
            'cookies': res.cookies,
            'encoding': res.encoding,
            'totalSeconds': res.elapsed.total_seconds()
        }
        self.result = result

        return result

    # 用例调试
    def case_debug(self):
        self.str_to_dict()
        # res = self.method_request()
        try:
            res = self.method_request()
        except Exception:
            raise ParameterException(msg='参数错误')
        result = self.get_result(res)

        return result

    @classmethod
    def case_log_search(cls, name, url, project, task, result, start, end, count=10, page=1):
        start_timeStamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))) * 1000 if start else None
        end_timeStamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))) * 1000 if end else None

        cases = mongo.db.easy.find(
            {
                'name': {'$regex': name} if name is not None else {'$regex': ''},
                'url': {'$regex': url} if url is not None else {'$regex': ''},
                'project_name': {'$regex': project} if project is not None else {'$regex': ''},
                'task_no': {'$regex': task} if task is not None else {'$regex': ''},
                'actual_result': result if result is not None else {'$type': 8},
                'create_time': {'$gt': start_timeStamp, '$lt': end_timeStamp} if start is not None else {'$type': 18}
            },
            {"_id": 0}).sort([('_id', -1)]).skip((page - 1) * count).limit(count)

        total = cases.count()

        cases = list(cases)

        return {
            'data': cases,
            'page': page,
            'pages': math.ceil(total / count),
            'count': count,
            'total': total
        }

    @classmethod
    def case_log_search_all(cls, task):
        cases = mongo.db.easy.find(
            {
                'task_no': {'$regex': task} if task is not None else {'$regex': ''},
            },
            {"_id": 0}).sort([('_id', -1)])

        return list(cases)

    @classmethod
    def case_log_remove(cls, name, url, project, task, result, start, end):
        start_timeStamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))) * 1000 if start else None
        end_timeStamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))) * 1000 if end else None
        result = mongo.db.easy.delete_many(
            {
                'name': {'$regex': name} if name is not None else {'$regex': ''},
                'url': {'$regex': url} if url is not None else {'$regex': ''},
                'project_name': {'$regex': project} if project is not None else {'$regex': ''},
                'task_no': {'$regex': task} if task is not None else {'$regex': ''},
                'actual_result': result if result is not None else {'$type': 8},
                'create_time': {'$gt': start_timeStamp, '$lt': end_timeStamp} if start is not None else {'$type': 18}
            }
        )

        return result.deleted_count
