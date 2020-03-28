""" 
@Time    : 2020/3/25 19:08
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 测试用例模型
"""
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, String, SmallInteger


class Case(Base):

    id = Column(Integer, primary_key=True, autoincrement=True, comment='用例id')
    name = Column(String(20), nullable=False, comment='用例名称 组内唯一不可重复')
    info = Column(String(50), comment='用例描述')
    url = Column(String(500), comment='请求地址')
    _method = Column('method', SmallInteger, nullable=False,comment='请求方法 ;  1 -> get |  2 -> post |  3 -> put |  4-> delete')
    _submit = Column('submit', SmallInteger, nullable=False,comment='提交方法 ;  1 -> json提交 |  2 -> 表单提交')
    header = Column(String(500), comment='请求头')
    data = Column(String(500), comment='请求头')
    _deal = Column('deal', SmallInteger, nullable=False, comment='后置处理方法 ;  1 -> 不做处理 |  2 -> 默认处理 |  3 -> 指定key获取数据 |  4-> 正则表达')
    condition = Column(String(50), comment='后置处理方法的条件语句，在后置处理方法为指定key或正则表达时为必填')
    expect_result = Column(String(500), comment='请求头')
    _type = Column('type', SmallInteger, nullable=False, comment='用例类型 ;  1 -> 接口自动化 |  2 -> UI自动化')
    case_group = Column(Integer, nullable=False, comment='用例分组id')
    create_user = Column(Integer, nullable=False, comment='用例创建人')
    update_user = Column(Integer, nullable=False, comment='用例修改人')
