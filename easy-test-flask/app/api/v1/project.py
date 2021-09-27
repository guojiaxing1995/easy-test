from flask import jsonify, current_app, request

from lin import login_required, route_meta, group_required
from lin.exception import Success, ParameterException
from lin.redprint import Redprint

from app.libs.enums import ProjectTypeEnum
from app.models.ConfigCopy import ConfigCopy
from app.models.project import Project
from app.validators.CaseForm import EnumTypeForm
from app.validators.ProjectForm import ProjectForm, ProjectConfigForm, CopyConfigForm, ProjectSearchForm, \
    ProjectPaginateForm

project_api = Redprint('project')


@project_api.route('', methods=['POST'])
@login_required
def create_project():
    form = ProjectForm().validate_for_api()
    Project.new_project(form)
    return Success(msg='新建工程成功')


@project_api.route('', methods=['GET'])
@route_meta('工程列表', module='工程')
@group_required
def get_projects():
    projects = Project.get_all()
    return jsonify(projects)


@project_api.route('/list', methods=['GET'])
@route_meta('工程列表', module='工程')
@group_required
def get_projects_paginate():
    form = ProjectPaginateForm().validate_for_api()
    projects = Project.get_all_paginate(form.name.data, form.page.data, form.count.data)
    return jsonify(projects)


@project_api.route('/search', methods=['GET'])
@login_required
def search_projects():
    form = ProjectSearchForm().validate_for_api()
    projects = Project.search(form.name.data)
    return jsonify(projects)


@project_api.route('/<pid>', methods=['PUT'])
@login_required
def update_project(pid):
    form = ProjectForm().validate_for_api()
    Project.edit_project(pid, form)
    return Success(msg='更新工程成功')


@project_api.route('/<pid>', methods=['DELETE'])
@route_meta('删除工程', module='工程')
@group_required
def delete_project(pid):
    Project.remove_project(pid)
    return Success(msg='删除工程成功')


@project_api.route('/auth', methods=['GET'])
@login_required
def get_auth_projects():
    """获取当前登陆用户的授权工程"""
    projects = Project.get_auth()
    return jsonify(projects)


@project_api.route('/type', methods=['GET'])
@login_required
def enum_type():
    form = EnumTypeForm().validate_for_api()
    if form.type.data == 'TYPE':
        return ProjectTypeEnum.data()
    else:
        raise ParameterException(msg='无目标类型')


@project_api.route('/saveConfig', methods=['POST'])
@route_meta('工程配置', module='工程')
@group_required
def save_config():
    form = ProjectConfigForm().validate_for_api()
    project = Project.query.filter_by(id=form.projectId.data).first()
    project.save_config(form.configs.data)
    return Success(msg='配置保存成功')


@project_api.route('/getConfig/<pid>', methods=['GET'])
@route_meta('工程配置', module='工程')
@group_required
def get_config(pid):
    project = Project.query.filter_by(id=pid).first()
    configs = project.get_configs()
    return jsonify(configs)


# 修改副本类型工程的用例信息
@project_api.route('/copyConfig', methods=['PUT'])
@route_meta('工程配置', module='工程')
@group_required
def copy_config():
    form = CopyConfigForm().validate_for_api()
    project = Project.query.filter_by(id=form.projectId.data).first_or_404()
    # 工程运行中不允许修改
    project.is_running()
    # 判断配置存在
    ConfigCopy.is_exist(form.id.data)
    config = ConfigCopy.query.filter_by(id=form.id.data).first()
    config.updateConfig(form.url.data, form.method.data, form.submit.data, form.header.data, form.data.data,
                        form.deal.data, form.condition.data, form.expect.data, form.assertion.data)

    return Success('修改配置成功')


@project_api.route('/userParam', methods=['POST'])
def set_user_parame():
    form = ProjectSearchForm().validate_for_api()
    project = Project.query.filter_by(id=form.id.data).first_or_404()
    project.set_user_parameters(form.userParam.data)

    return Success('参数设置成功')


@project_api.route('/userParam', methods=['GET'])
def get_user_parame():
    form = ProjectSearchForm().validate_for_api()
    project = Project.query.filter_by(id=form.id.data).first_or_404()
    parame = project.get_user_parameters()

    return jsonify(parame)
