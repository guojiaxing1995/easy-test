"""
@Time    : 2020/3/25 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 测试用例模型
"""
import math
import operator
import os
import shutil
import time
from datetime import datetime
import json
import re
import requests
from flask import current_app
from flask_jwt_extended import current_user, get_current_user
from lin import manager
from lin.exception import ParameterException, AuthFailed
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger, between
from lin.db import db

from app.libs.case_log import log, edit_log
from app.libs.deal import deal_default, get_target_value
from app.libs.enums import CaseMethodEnum, CaseSubmitEnum, CaseDealEnum, CaseTypeEnum, CaseAssertEnum, UserAuthEnum, \
    ProjectTypeEnum, CaseExcelEnum
from app.libs.error_code import CaseRemoveException, CaseUploadExcelException, CaseDownloadException
from app.libs.init import mongo
from app.libs.opreation_excel import OperationExcel
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
    data = Column(String(3000), comment='请求体')
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

        old_case = Case(self.case_group, self.name, self.info, self.url, self.method, self.submit, self.header,
                        self.data, self.deal, self.condition, self.expect, self.assertion, self.type)
        old_case.id = self.id

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

        self.edit_log(old_case)

    # 记录修改日志
    def edit_log(self, old_case):
        id = self.id
        name = {'val': self.name, 'modify': True} if self.name != old_case.name else {'val': self.name, 'modify': False}
        info = {'val': self.info, 'modify': True} if self.info != old_case.info else {'val': self.info, 'modify': False}
        url = {'val': self.url, 'modify': True} if self.url != old_case.url else {'val': self.url, 'modify': False}
        method = {'val': self.method, 'modify': True} if self.method != old_case.method \
            else {'val': self.method, 'modify': False}
        submit = {'val': self.submit, 'modify': True} if self.submit != old_case.submit \
            else {'val': self.submit, 'modify': False}
        header = {'val': self.header, 'modify': True} if self.header != old_case.header \
            else {'val': self.header, 'modify': False}
        data = {'val': self.data, 'modify': True} if self.data != old_case.data else {'val': self.data, 'modify': False}
        deal = {'val': self.deal, 'modify': True} if self.deal != old_case.deal else {'val': self.deal, 'modify': False}
        condition = {'val': self.condition, 'modify': True} if self.condition != old_case.condition \
            else {'val': self.condition, 'modify': False}
        expect = {'val': self.expect, 'modify': True} if self.expect != old_case.expect \
            else {'val': self.expect, 'modify': False}
        assertion = {'val': self.assertion, 'modify': True} if self.assertion != old_case.assertion \
            else {'val': self.assertion, 'modify': False}
        type = {'val': self.type, 'modify': True} if self.type != old_case.type else {'val': self.type, 'modify': False}
        case_group = {'val': self.case_group, 'modify': True} if self.case_group != old_case.case_group \
            else {'val': self.case_group, 'modify': False}

        if name['modify'] or info['modify'] or url['modify'] or method['modify'] or submit['modify'] \
                or header['modify'] or data['modify'] or deal['modify'] or condition['modify'] or expect['modify'] \
                or assertion['modify'] or type['modify'] or case_group['modify']:
            log = edit_log(id, name, info, url, method, submit, header, data, deal, condition, expect, assertion, type,
                           case_group)

            mongo.db.modify.insert(log)

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
        results = cls.query.join(CaseGroup, CaseGroup.id == cls.case_group). \
            join(manager.user_model, manager.user_model.id == cls.create_user).filter(
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
            CaseGroup.name.label('group_name'),
            manager.user_model.username.label('create_user'),
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
        except Exception as e:
            self.actual_result = False
            self.reason = str(e)
            current_app.logger.debug(self.reason)

        # 更新task表 成功、失败
        self.update_task_result(task)
        # 用例执行日志插入mongoDB数据库
        case_log = log(self, project, task, create_user)
        mongo.db.easy.insert(case_log)
        # 向客户端广播用例日志
        api_server = current_app.config.get('API_SERVER')
        res = requests.get(url=api_server + '/v1/task/log/' + str(task.task_no))
        current_app.logger.debug(res.text)

    # 拼接请求地址
    def stitch_url(self, server):
        if 'http' not in server:
            server = 'http://' + server
        if 'http' not in self.url:
            self.url = server + self.url

    # 找到${var} 替换变量的值
    # re.search(r'\${(.*)\}','/v1/${job}o').group(0)  '${job}' |  re.search(r'\${(.*)\}','/v1/${job}o').group(1)  'job'
    def var_substitution(self, var_dick):
        # url 处理
        url_var = re.search(r'\${(.*)\}', self.url)
        if url_var:
            try:
                var = var_dick[url_var.group(1)]
            except Exception:
                # 如果变量不在全局字典中则赋值变量为 ''
                current_app.logger.debug('变量【' + url_var.group(1) + '】不在工程全局字典中')
                var = ''
            self.url = self.url.replace(url_var.group(0), str(var))
        # header 处理
        if self.header:
            for key, value in self.header.items():
                if type(value) == str:
                    header_var = re.search(r'\${(.*)\}', value)
                    if header_var:
                        try:
                            self.header[key] = var_dick[header_var.group(1)]
                        except Exception:
                            # 如果变量不在全局字典中则赋值变量为 None
                            current_app.logger.debug('变量【' + header_var.group(1) + '】不在工程全局字典中')
                            self.header[key] = None
        # data 处理
        if self.data:
            for key, value in self.data.items():
                if type(value) == str:
                    data_var = re.search(r'\${(.*)\}', value)
                    if data_var:
                        try:
                            self.data[key] = var_dick[data_var.group(1)]
                        except Exception:
                            # 如果变量不在全局字典中则赋值变量为 None
                            current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                            self.data[key] = None
                # 处理value为列表的情况
                if type(value) == list:
                    for i in range(len(value)):
                        if type(value[i]) == str:
                            data_var = re.search(r'\${(.*)\}', value[i])
                            if data_var:
                                try:
                                    self.data[key][i] = var_dick[data_var.group(1)]
                                except Exception:
                                    # 如果变量不在全局字典中则赋值变量为 None
                                    current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                                    self.data[key][i] = None

                # 处理value为字典的情况
                if type(value) == dict:
                    for key_second, value_second in value.items():
                        if type(value_second) == str:
                            data_var = re.search(r'\${(.*)\}', value_second)
                            if data_var:
                                try:
                                    self.data[key][key_second] = var_dick[data_var.group(1)]
                                except Exception:
                                    # 如果变量不在全局字典中则赋值变量为 None
                                    current_app.logger.debug('变量【' + data_var.group(1) + '】不在工程全局字典中')
                                    self.data[key][key_second] = None

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
                if len(item.split(',')) > 1:
                    new_key = item.split(',')[1]
                else:
                    new_key = None
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
            # 'cookies': res.cookies,
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
        except Exception as e:
            current_app.logger.debug(e)
            raise ParameterException(msg='参数错误')
        result = self.get_result(res)

        return result

    @classmethod
    def case_log_search(cls, cid, name, url, project, task, result, start, end, count=10, page=1):
        start_timeStamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))) * 1000 if start else None
        end_timeStamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))) * 1000 if end else None

        cases = mongo.db.easy.find(
            {
                'id': cid if cid is not None else {'$type': 16},
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

    @classmethod
    def group_by_case_group(cls):
        from app.models.CaseGroup import CaseGroup
        groups = CaseGroup.query.filter_by(delete_time=None).all()
        for group in groups:
            group.hide('info', 'create_time', 'update_time')
            cases = cls.query.filter_by(case_group=group.id, delete_time=None).all()
            for case in cases:
                case.hide('info', 'url', 'method', 'submit', 'header', 'data', 'deal', 'condition', 'expect',
                          'type', 'assertion', 'case_group', 'create_user', 'update_user', 'create_time', 'update_time')
            setattr(group, 'cases', cases)
            group._fields.append('cases')

        return groups

    @classmethod
    def search_edit_logs(cls, cid, url, method, deal, start, end, count=10, page=1):
        start_timeStamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))) * 1000 if start else None
        end_timeStamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))) * 1000 if end else None

        edit_logs = mongo.db.modify.find(
            {
                'id': int(cid),
                'url.val': {'$regex': url} if url is not None else {'$regex': ''},
                'method.val': int(method) if method is not None else {'$type': 16},
                'deal.val': int(deal) if deal is not None else {'$type': 16},
                'create_time': {'$gt': start_timeStamp, '$lt': end_timeStamp} if start is not None else {'$type': 18}
            },
            {"_id": 0}).sort([('_id', -1)]).skip((page - 1) * count).limit(count)

        total = edit_logs.count()

        edit_logs = list(edit_logs)

        return {
            'data': edit_logs,
            'page': page,
            'pages': math.ceil(total / count),
            'count': count,
            'total': total
        }

    @classmethod
    def edit_logs_remove(cls, cid, url, method, deal, start, end):
        start_timeStamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S"))) * 1000 if start else None
        end_timeStamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S"))) * 1000 if end else None

        result = mongo.db.modify.delete_many(
            {
                'id': int(cid),
                'url.val': {'$regex': url} if url is not None else {'$regex': ''},
                'method.val': int(method) if method is not None else {'$type': 16},
                'deal.val': int(deal) if deal is not None else {'$type': 16},
                'create_time': {'$gt': start_timeStamp, '$lt': end_timeStamp} if start is not None else {'$type': 18}
            }
        )

        return result.deleted_count

    # 获取某个用户的数据, 未指定用户则获取当前用户
    @classmethod
    def user_case(cls, uid, name, page, count):
        count = int(count) if count else current_app.config.get('COUNT_DEFAULT')
        page = int(page) if page else current_app.config.get('PAGE_DEFAULT') + 1
        from app.models.CaseGroup import CaseGroup
        if not uid:
            uid = current_user.id
        results = cls.query.join(CaseGroup, CaseGroup.id == cls.case_group). \
            join(manager.user_model, manager.user_model.id == cls.create_user).filter(
            cls.create_user == uid,
            cls.name.like(f'%{name}%') if name is not None else '',
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
            CaseGroup.name.label('group_name'),
            manager.user_model.username.label('create_user'),
        ).order_by(
            text('Case.update_time desc')
        ).paginate(page, count)

        items = [dict(zip(result.keys(), result)) for result in results.items]
        results.items = items
        data = paging(results)
        return data

    # 用例统计
    def log_collect(self):
        true_count = mongo.db.easy.find(
            {
                'id': self.id,
                'actual_result': True
            },
            {"_id": 0}).sort([('_id', -1)]).count()

        false_count = mongo.db.easy.find(
            {
                'id': self.id,
                'actual_result': False
            },
            {"_id": 0}).sort([('_id', -1)]).count()

        last_modify_log = mongo.db.modify.find(
            {
                'id': self.id,
            },
            {"_id": 0, 'create_time': 1}).sort([('_id', -1)]).limit(1)

        last_modify_time = None
        last_modify_log = list(last_modify_log)
        if last_modify_log:
            last_modify_time = last_modify_log[0]['create_time']

        edit_count = mongo.db.modify.find(
            {
                'id': self.id,
            },
            {"_id": 0}).sort([('_id', -1)]).count()

        return {
            'true_count': true_count,
            'false_count': false_count,
            'count': true_count + false_count,
            'last_modify_time': last_modify_time,
            'edit_count': edit_count
        }

    def used_by_project(self):
        from app.models.ConfigCopy import ConfigCopy
        from app.models.ConfigRelation import ConfigRelation
        pid_list = []
        copy_configs = ConfigCopy.query.filter_by(case_id=self.id, delete_time=None).all()
        for config in copy_configs:
            pid_list.append(config.project_id)

        relation_configs = ConfigRelation.query.filter_by(case_id=self.id, delete_time=None).all()
        for config in relation_configs:
            pid_list.append(config.project_id)

        project_list = []
        for pid in pid_list:
            from app.models.project import Project
            project = Project.query.filter_by(id=pid).first()
            p = {
                'name': project.name,
                'id': pid,
                'type': project.type,
                'type_name': ProjectTypeEnum.data()[project.type],
            }
            project_list.append(p)

        return project_list

    # 用例总数
    @classmethod
    def total(cls):
        return cls.query.filter_by(delete_time=None).count()

    # 今日新增用例数
    @classmethod
    def today(cls):

        add = db.session.execute("SELECT * FROM `easy-test`.`case` where delete_time is null "
                                 "and DATE_FORMAT(create_time,'%Y-%m-%d') = DATE_FORMAT(NOW(),'%Y-%m-%d')")
        return len(list(add))

    # 执行次数top
    @classmethod
    def top(cls):
        total_top_pipeline = [
            {
                '$group': {
                    '_id': {
                        'id': '$id',
                        'name': '$name',
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            },
            {
                '$sort': {
                    'count': -1
                }
            },
            {
                '$limit': 10
            }
        ]
        total_top = mongo.db.easy.aggregate(total_top_pipeline)
        total_top = list(total_top)
        for t in total_top:
            t['name'] = t['_id']['name']
            t.pop('_id')

        total_pipeline = [
            {
                '$group': {
                    '_id': {
                        'id': '$id',
                        'name': '$name',
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        total_test = mongo.db.easy.aggregate(total_pipeline)
        total_test = list(total_test)
        pass_pipeline = [
            {
                '$match': {
                    'actual_result': True
                }
            },
            {
                '$group': {
                    '_id': {
                        'id': '$id',
                        'name': '$name',
                    },
                    'count': {
                        '$sum': 1
                    }
                }
            }
        ]
        pass_test = mongo.db.easy.aggregate(pass_pipeline)
        pass_test = list(pass_test)

        pass_rate = []

        for t in total_test:
            t_copy = t
            t_copy['name'] = t['_id']['name']
            t_copy['pass'] = 0
            t_copy['rate'] = 0
            for p in pass_test:
                if t['_id']['id'] == p['_id']['id']:
                    t_copy['pass'] = p['count']
                    t_copy['rate'] = float(format(float(t_copy['pass']) / float(t_copy['count']) * 100, '.2f'))
                    continue
            t_copy.pop('_id')
            pass_rate.append(t_copy)

        # 按通过率排序
        length = len(pass_rate)
        for index in range(length):
            # 标志位
            flag = True
            for j in range(1, length - index):
                if pass_rate[j - 1]['rate'] < pass_rate[j]['rate']:
                    pass_rate[j - 1], pass_rate[j] = pass_rate[j], pass_rate[j - 1]
                    flag = False
            if flag:
                # 没有发生交换，直接返回list
                break

        if len(pass_rate) > 10:
            pass_rate = pass_rate[0:10]

        return {
            'total_top': total_top,
            'pass_rate_top': pass_rate
        }

    @classmethod
    def upload_add(cls, file_path):
        excel = OperationExcel(file_path)
        excel.get_table()
        excel.get_rowNum()
        excel.get_colNum()
        if excel.colNum < 12:
            raise CaseUploadExcelException('上传模板格式错误，请检查')
        if excel.rowNum <= 1:
            raise CaseUploadExcelException('用例数据不存在')

        for row in range(1, excel.rowNum):
            # 用例名称
            name = excel.get_cell_value(row, CaseExcelEnum.NAME.value)
            if not name:
                raise CaseUploadExcelException('用例名称不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.NAME.value + 1) + '列')
            # 用例分组
            group = excel.get_cell_value(row, CaseExcelEnum.GROUP.value)
            if not group:
                raise CaseUploadExcelException('分组名称不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.GROUP.value + 1) + '列')
            from app.models.CaseGroup import CaseGroup
            case_group = CaseGroup.query.filter_by(name=group, delete_time=None).first()
            if not case_group:
                raise CaseUploadExcelException('分组不存在，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.GROUP.value + 1) + '列')

            if Case.query.filter_by(name=name, case_group=case_group.id, delete_time=None).first():
                raise CaseUploadExcelException('同一组已存在相同用例名称，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.NAME.value + 1) + '列')
            # 请求地址
            url = excel.get_cell_value(row, CaseExcelEnum.URL.value)
            if not url:
                raise CaseUploadExcelException('URL不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.URL.value + 1) + '列')
            # 请求方法
            method = excel.get_cell_value(row, CaseExcelEnum.METHOD.value)
            if not method:
                raise CaseUploadExcelException('请求方法不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.METHOD.value + 1) + '列')
            if method == CaseMethodEnum.GET.name:
                method_code = CaseMethodEnum.GET.value
            elif method == CaseMethodEnum.POST.name:
                method_code = CaseMethodEnum.POST.value
            elif method == CaseMethodEnum.PUT.name:
                method_code = CaseMethodEnum.PUT.value
            elif method == CaseMethodEnum.DELETE.name:
                method_code = CaseMethodEnum.DELETE.value
            else:
                raise CaseUploadExcelException('请求方法填写错误，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.METHOD.value + 1) + '列')
            # 请求体
            body = excel.get_cell_value(row, CaseExcelEnum.DATA.value)
            # 请求头
            header = excel.get_cell_value(row, CaseExcelEnum.HEADER.value)
            # 请求方式
            submit = excel.get_cell_value(row, CaseExcelEnum.SUBMIT.value)
            if not submit:
                raise CaseUploadExcelException('提交方式不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.SUBMIT.value + 1) + '列')
            if submit == CaseSubmitEnum.JSON.name:
                submit_code = CaseSubmitEnum.JSON.value
            elif submit == CaseSubmitEnum.FORM.name:
                submit_code = CaseSubmitEnum.FORM.value
            else:
                raise CaseUploadExcelException('提交方式填写错误，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.SUBMIT.value + 1) + '列')
            # 后置处理
            deal = excel.get_cell_value(row, CaseExcelEnum.DEAL.value)
            if not deal:
                raise CaseUploadExcelException('处理方法不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.DEAL.value + 1) + '列')
            if deal == CaseDealEnum.NOT.name:
                deal_code = CaseDealEnum.NOT.value
            elif deal == CaseDealEnum.JSON.name:
                deal_code = CaseDealEnum.JSON.value
            elif deal == CaseDealEnum.DEFAULT.name:
                deal_code = CaseDealEnum.DEFAULT.value
            elif deal == CaseDealEnum.REGULAR.name:
                deal_code = CaseDealEnum.REGULAR.value
            else:
                raise CaseUploadExcelException('处理方法填写错误，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.DEAL.value + 1) + '列')
            # 处理语句
            condition = excel.get_cell_value(row, CaseExcelEnum.CONDITION.value)
            # 断言方式
            assertion = excel.get_cell_value(row, CaseExcelEnum.ASSERTION.value)
            if not assertion:
                raise CaseUploadExcelException('断言方法不能为空，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.ASSERTION.value + 1) + '列')
            if assertion == CaseAssertEnum.EQUAL.name:
                assertion_code = CaseAssertEnum.EQUAL.value
            elif assertion == CaseAssertEnum.NOTEQUAL.name:
                assertion_code = CaseAssertEnum.NOTEQUAL.value
            elif assertion == CaseAssertEnum.IN.name:
                assertion_code = CaseAssertEnum.IN.value
            elif assertion == CaseAssertEnum.NOTIN.name:
                assertion_code = CaseAssertEnum.NOTIN.value
            elif assertion == CaseAssertEnum.SUCCESS.name:
                assertion_code = CaseAssertEnum.SUCCESS.value
            else:
                raise CaseUploadExcelException('断言方法填写错误，第' +
                                               str(row + 1) + '行第' + str(CaseExcelEnum.ASSERTION.value + 1) + '列')
            # 期望结果
            expection = excel.get_cell_value(row, CaseExcelEnum.EXPECTION.value)
            # 描述
            info = excel.get_cell_value(row, CaseExcelEnum.INFO.value)

            case = Case(case_group.id, name, info, url, method_code, submit_code, header, body, deal_code, condition,
                        expection, assertion_code)

            db.session.add(case)
            db.session.flush()
        db.session.commit()

    @classmethod
    def case_download_search(cls, name, url, case_group, start, end, cid, method, deal):
        # auths = UserAuth.query.filter_by(user_id=current_user.id, _type=UserAuthEnum.GROUP.value).all()
        # gids = [auth.auth_id for auth in auths]
        from app.models.CaseGroup import CaseGroup
        results = cls.query.join(CaseGroup, CaseGroup.id == cls.case_group). \
            join(manager.user_model, manager.user_model.id == cls.create_user).filter(
            cls.id == cid if cid else '',
            cls._method == method if method else '',
            cls._deal == deal if deal else '',
            cls.case_group == case_group if case_group else '',
            cls.name.like(f'%{name}%') if name is not None else '',
            cls.url.like(f'%{url}%') if url is not None else '',
            cls._update_time.between(start, end) if start and end else '',
            # cls.case_group.in_(gids) if current_user.id != 1 else '',
            cls.delete_time == None,
        ).with_entities(
            cls.name,
            CaseGroup.name.label('group_name'),
            cls.url,
            cls._method.label('method'),
            cls.data,
            cls.header,
            cls._submit.label('submit'),
            cls._deal.label('deal'),
            cls.condition,
            cls._assertion.label('assertion'),
            cls.expect.label('expect'),
            cls.info,
        ).order_by(
            text('Case.update_time desc')
        ).all()

        if len(results) == 0:
            raise CaseDownloadException('无导出数据')
        elif len(results) > 300:
            raise CaseDownloadException('导出用例条数过大，导出用例数需小于300条')

        return results

    @staticmethod
    def copy_excel_template():
        directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/excel/template'
        template_filename = 'caseUploadTemplate.xlsx'
        download_filename = 'caseDownload_' + str(int(round(time.time()) * 1000)) + '.xls'
        # 复制用例下载模板作为被写入的文件
        shutil.copyfile(directory + '/' + template_filename, directory + '/' + download_filename)

        return directory + '/' + download_filename, directory, download_filename

    @classmethod
    def write_case_excel(cls, cases, file_path):
        excel = OperationExcel(file_path)
        excel.get_sheet_write()
        for row in range(len(cases)):
            for col in range(len(cases[row])):
                if col == CaseExcelEnum.METHOD.value:
                    excel.write_execel(row+1, col, CaseMethodEnum(cases[row][col]).name)
                elif col == CaseExcelEnum.SUBMIT.value:
                    excel.write_execel(row+1, col, CaseSubmitEnum(cases[row][col]).name)
                elif col == CaseExcelEnum.DEAL.value:
                    excel.write_execel(row+1, col, CaseDealEnum(cases[row][col]).name)
                elif col == CaseExcelEnum.ASSERTION.value:
                    excel.write_execel(row+1, col, CaseAssertEnum(cases[row][col]).name)
                else:
                    excel.write_execel(row+1, col, cases[row][col])
        excel.write_save()
