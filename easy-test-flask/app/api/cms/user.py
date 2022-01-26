"""
    user apis
    ~~~~~~~~~
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from operator import and_

import requests
from flask import jsonify, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, get_current_user, \
    create_refresh_token, verify_jwt_refresh_token_in_request
from lin.core import manager, route_meta, Log
from lin.db import db
from lin.enums import UserAdmin, UserActive
from lin.exception import NotFound, Success, Failed, RepeatException, ParameterException, AuthFailed
from lin.jwt import login_required, admin_required, get_tokens
from lin.log import Logger
from lin.redprint import Redprint

from app.libs.error_code import RefreshException
from app.libs.utils import json_res, pinyin, group_by_initials
from app.models.UserAuth import UserAuth
from app.validators.CaseForm import UserGroupAuthForm
from app.validators.forms import LoginForm, RegisterForm, ChangePasswordForm, UpdateInfoForm, \
    AvatarUpdateForm, LoginMiniForm, BindMiniForm

user_api = Redprint('user')


@user_api.route('/register', methods=['POST'])
@route_meta(auth='注册', module='用户', mount=False)
@Logger(template='管理员新建了一个用户')  # 记录日志
@admin_required
def register():
    form = RegisterForm().validate_for_api()
    user = manager.find_user(username=form.username.data)
    if user:
        raise RepeatException(msg='用户名重复，请重新输入')
    if form.email.data and form.email.data.strip() != "":
        user = manager.user_model.query.filter(and_(
            manager.user_model.email.isnot(None),
            manager.user_model.email == form.email.data
        )).first()
        if user:
            raise RepeatException(msg='注册邮箱重复，请重新输入')
    _register_user(form)
    return Success(msg='用户创建成功')


@user_api.route('/login', methods=['POST'])
@route_meta(auth='登陆', module='用户', mount=False)
def login():
    form = LoginForm().validate_for_api()
    user = manager.user_model.verify(form.username.data, form.password.data)
    # 此处不能用装饰器记录日志
    Log.create_log(
        message=f'{user.username}登陆成功获取了令牌',
        user_id=user.id, user_name=user.username,
        status_code=200, method='post', path='/cms/user/login',
        authority='无', commit=True
    )
    access_token, refresh_token = get_tokens(user)
    return json_res(access_token=access_token, refresh_token=refresh_token)


@user_api.route('', methods=['PUT'])
@route_meta(auth='用户更新信息', module='用户', mount=False)
@login_required
def update():
    form = UpdateInfoForm().validate_for_api()
    user = get_current_user()
    if form.email.data and user.email != form.email.data:
        exists = manager.user_model.get(email=form.email.data)
        if exists:
            raise ParameterException(msg='邮箱已被注册，请重新输入邮箱')
    with db.auto_commit():
        user.email = form.email.data
        user.nickname = form.nickname.data
    return Success(msg='操作成功')


@user_api.route('/change_password', methods=['PUT'])
@route_meta(auth='修改密码', module='用户', mount=False)
@Logger(template='{user.username}修改了自己的密码')  # 记录日志
@login_required
def change_password():
    form = ChangePasswordForm().validate_for_api()
    user = get_current_user()
    ok = user.change_password(form.old_password.data, form.new_password.data)
    if ok:
        db.session.commit()
        return Success(msg='密码修改成功')
    else:
        return Failed(msg='修改密码失败')


@user_api.route('/information', methods=['GET'])
@route_meta(auth='查询自己信息', module='用户', mount=False)
@login_required
def get_information():
    current_user = get_current_user()
    group_name = db.session.query(manager.group_model.name).filter_by(id=current_user.group_id).first()
    group_name = group_name[0] if group_name else None
    setattr(current_user, 'group_name', group_name)
    current_user._fields.append('group_name')
    return jsonify(current_user)


@user_api.route('/refresh', methods=['GET'])
@route_meta(auth='刷新令牌', module='用户', mount=False)
def refresh():
    try:
        verify_jwt_refresh_token_in_request()
    except Exception:
        return RefreshException()

    identity = get_jwt_identity()
    if identity:
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return json_res(access_token=access_token, refresh_token=refresh_token)

    return NotFound(msg='refresh_token未被识别')


@user_api.route('/auths', methods=['GET'])
@route_meta(auth='查询自己拥有的权限', module='用户', mount=False)
@login_required
def get_allowed_apis():
    user = get_current_user()
    group_name = db.session.query(manager.group_model.name).filter_by(id=user.group_id).first()
    group_name = group_name[0] if group_name else None
    setattr(user, 'group_name', group_name)
    user._fields.append('group_name')
    auths = db.session.query(
        manager.auth_model.auth, manager.auth_model.module
    ).filter_by(soft=False, group_id=user.group_id).all()
    auths = [{'auth': auth[0], 'module': auth[1]} for auth in auths]
    from .admin import _split_modules
    res = _split_modules(auths)
    setattr(user, 'auths', res)
    user._fields.append('auths')
    return jsonify(user)


@user_api.route('/avatar', methods=['PUT'])
@login_required
def set_avatar():
    form = AvatarUpdateForm().validate_for_api()
    user = get_current_user()
    with db.auto_commit():
        user._avatar = form.avatar.data
    return Success(msg='更新头像成功')


def _register_user(form: RegisterForm):
    with db.auto_commit():
        # 注意：此处使用挂载到manager上的user_model，不可使用默认的User
        user = manager.user_model()
        user.username = form.username.data
        if form.email.data and form.email.data.strip() != "":
            user.email = form.email.data
        user.password = form.password.data
        user.group_id = form.group_id.data
        db.session.add(user)


# 按照分组返回所有用户
@user_api.route('/userByGroup', methods=['GET'])
@login_required
def user_by_group():
    groups = manager.group_model.get(one=False)
    if groups is None:
        raise NotFound(msg='不存在任何权限组')

    for group in groups:
        users = manager.user_model.query.filter().filter_by(group_id=group.id).all()
        if users:
            for user in users:
                user.hide('active', 'admin', 'group_id', 'update_time', 'create_time')
            setattr(group, 'users', users)
            group._fields.append('users')

    return jsonify(groups)


# 按照用户权限分组返回所有用户 并显示目标类型权限授权情况
@user_api.route('/userAuthByGroup', methods=['GET'])
@login_required
def user_auth_by_group():
    form = UserGroupAuthForm().validate_for_api()
    user_groups = manager.group_model.get(one=False)
    if user_groups is None:
        raise NotFound(msg='不存在任何用户组')

    for user_group in user_groups:
        users = manager.user_model.query.filter().filter_by(group_id=user_group.id).all()
        if users:
            for user in users:
                # 如果传入权限分组和权限类型则返回对应用户是否获取到授权
                if form.authId.data:
                    # 查询权限表看当前循环用户是否有权限
                    auth = UserAuth.get_user_auth(user.id, form.authId.data, form.authType.data)
                    if auth:
                        setattr(user, 'permission', True)
                        user._fields.append('permission')
                    else:
                        setattr(user, 'permission', False)
                        user._fields.append('permission')
                else:
                    setattr(user, 'permission', False)
                    user._fields.append('permission')
                user.hide('active', 'admin', 'group_id', 'update_time', 'create_time')
            setattr(user_group, 'users', users)
            user_group._fields.append('users')

    return jsonify(user_groups)


# 按照首字母分组返回用户以及对应用户目标权限的授权情况
@user_api.route('/userByInitials', methods=['GET'])
@login_required
def user_by_initials():
    form = UserGroupAuthForm().validate_for_api()
    # 获取首字母列表以及 首字母分组模板列表
    users_by_initials, letters = group_by_initials()
    others = []
    users = manager.user_model.query.filter_by(delete_time=None, admin=UserAdmin.COMMON.value,
                                               active=UserActive.ACTIVE.value).all()
    for user in users:
        # 如果传入权限分组和权限类型则返回对应用户是否获取到授权
        if form.authId.data:
            # 查询权限表看当前循环用户是否有权限
            auth = UserAuth.get_user_auth(user.id, form.authId.data, form.authType.data)
            if auth:
                setattr(user, 'permission', True)
                user._fields.append('permission')
            else:
                setattr(user, 'permission', False)
                user._fields.append('permission')
        else:
            setattr(user, 'permission', False)
            user._fields.append('permission')
        user.hide('active', 'admin', 'group_id', 'update_time', 'create_time')
        name_pinyin = pinyin(user.username)
        first = name_pinyin[:1].upper()
        if first not in letters:
            others.append(user)
        else:
            for item in users_by_initials:
                if item['name'] == first:
                    item['users'].append(user)
    users_by_initials.append({'name': '其他', 'users': others})

    return jsonify(users_by_initials)


# 小程序登录
@user_api.route('/login/mini', methods=['POST'])
def login_mini():
    form = LoginMiniForm().validate_for_api()
    appid = current_app.config.get('APP_ID')
    secret = current_app.config.get('APP_SECRET')
    code = form.code.data
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + \
          '&grant_type=authorization_code'
    res = requests.get(url)
    if 'openid' not in res.json().keys():
        return Failed('小程序用户异常')
    openid = res.json()['openid']
    user = manager.user_model.query.filter_by(openid=openid).first_or_404()
    # 此处不能用装饰器记录日志
    Log.create_log(
        message=f'{user.username}小程序登陆成功获取了令牌',
        user_id=user.id, user_name=user.username,
        status_code=200, method='post', path='/cms/user/login/mini',
        authority='无', commit=True
    )
    access_token, refresh_token = get_tokens(user)
    return json_res(access_token=access_token, refresh_token=refresh_token)


# 小程序账号和业务系统账户绑定
@user_api.route('/bind/mini', methods=['POST'])
def bind_mini():
    form = BindMiniForm().validate_for_api()
    user = manager.user_model.verify(form.username.data, form.password.data)

    appid = current_app.config.get('APP_ID')
    secret = current_app.config.get('APP_SECRET')
    code = form.code.data
    url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + \
          '&grant_type=authorization_code'
    res = requests.get(url)
    if 'openid' not in res.json().keys():
        return Failed('小程序用户异常')
    openid = res.json()['openid']
    if manager.user_model.query.filter_by(openid=openid).first():
        return Failed('小程序已经与其他账号绑定')
    if user.openid:
        return Failed('当前账号已经被其他用户绑定')
    with db.auto_commit():
        user.openid = openid

    return Success('绑定成功')
