"""
@Time    : 2020/4/18 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : ConfigCopy.py
@Desc    : 工程配置-副本
"""
from flask import current_app
from lin import db
from lin.exception import UnknownException
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Boolean, String, SmallInteger

from app.libs.enums import CaseMethodEnum, CaseSubmitEnum, CaseDealEnum, CaseAssertEnum, CaseTypeEnum
from app.libs.error_code import ConfigNotFound
from app.models.case import Case
from app.models.task import Task


class ConfigCopy(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='配置id')
    project_id = Column(Integer, nullable=False, comment='工程id')
    order = Column(Integer, nullable=False, comment='执行顺序')
    is_run = Column(Boolean, nullable=False, default=True, comment='是否执行')
    case_id = Column(Integer, nullable=False, comment='用例id')
    name = Column(String(20), nullable=False, comment='用例名称')
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

    def __init__(self, project_id, order, case_id, name, is_run=True, info=None, url=None, method=1, submit=1,
                 header=None,
                 data=None, deal=1, condition=None, expect=None, assertion=1, case_type=1):
        super().__init__()
        self.project_id = project_id
        self.order = order
        self.case_id = case_id
        self.name = name
        self.is_run = is_run
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

    @classmethod
    def get_configs(cls, project_id):
        return cls.query.filter_by(project_id=project_id).order_by(cls.order).all()

    @classmethod
    def copy_config(cls, project_id, configs):
        # 获取新config id 列表(不包含需要新增的配置)
        new_config_ids = [config[0] for config in configs if config[0]]
        # 获取原config id 列表
        config_ids = cls.query.filter_by(project_id=project_id).with_entities(cls.id).all()
        old_config_ids = [list(x)[0] for x in config_ids]
        # 需要删除的config id 列表
        delete_config_ids = list(set(old_config_ids).difference(set(new_config_ids)))
        # 需要新增的配置
        add_configs = [config for config in configs if config[0] is None]
        # 需要修改的配置（原配置 已经除去被删除 且不包括新增配置）
        update_configs = [config for config in configs if config[0]]

        try:
            # 删除config
            if delete_config_ids:
                for cid in delete_config_ids:
                    config = cls.query.filter_by(id=cid, project_id=project_id).first_or_404()
                    db.session.delete(config)
                db.session.flush()

            # 新增config
            if add_configs:
                for c in add_configs:
                    case_id = c[1]
                    is_run = c[2]
                    order = c[3]
                    case = Case.query.filter_by(id=case_id).first_or_404()
                    config = cls(project_id, order, case_id, case.name, is_run, case.info, case.url, case.method,
                                 case.submit, case.header, case.data, case.deal, case.condition, case.expect,
                                 case.assertion, case.type)
                    db.session.add(config)
                db.session.flush()

            # 修改原用例（非新增） 是否执行 排序
            if update_configs:
                for c in update_configs:
                    config_id = c[0]
                    is_run = c[2]
                    order = c[3]
                    config = cls.query.filter_by(id=config_id).first_or_404()
                    config.is_run = is_run
                    config.order = order
                db.session.flush()

            db.session.commit()
        except Exception:
            db.session.rollback()
            raise UnknownException(msg='修改配置异常')

    @classmethod
    def is_exist(cls, cid):
        config = cls.query.filter_by(id=cid).first()
        if not config:
            raise ConfigNotFound(msg='配置不存在，请先保存配置')

    #  修改副本类型配置用例信息
    def updateConfig(self, url, method, submit, header, data, deal, condition, expect, assertion):
        try:
            self.url = url
            self.method = CaseMethodEnum(method)
            self.submit = CaseSubmitEnum(submit)
            self.header = header
            self.data = data
            self.deal = CaseDealEnum(deal)
            self.condition = condition
            self.expect = expect
            self.assertion = CaseAssertEnum(assertion)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise UnknownException(msg='修改配置异常')

    # 批量执行
    @classmethod
    def batch(cls, project):
        project.var_dick = {}
        configs = cls.query.filter_by(project_id=project.id, is_run=True).order_by(cls.order).all()
        if not configs:
            raise ConfigNotFound(msg='工程下无可运行用例')
        # 执行用例总数
        total = len(configs)
        task = Task(project.id, 1, total)
        task.new_task()
        step = 100 / total
        progress = 0
        with db.session.no_autoflush:
            for config in configs:
                case = Case(0, config.name, config.info, config.url, config.method, config.submit, config.header,
                            config.data, config.deal, config.condition, config.expect, config.assertion, config.type)
                case.id = config.case_id
                case.execute_one(project, task)
                progress += step
                # 更新工程进度
                project.update_progress(progress)
        project.update_progress(100)
