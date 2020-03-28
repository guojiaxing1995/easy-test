""" 
@Time    : 2020/3/21 10:36
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : 用例视图
"""
from flask import jsonify
from lin import manager
from lin.exception import NotFound
from lin.redprint import Redprint
from lin import route_meta, group_required, login_required

from app.models.UserAuth import UserAuth
from app.validators.CaseForm import UserGroupAuthForm

case_api = Redprint('case')

#按照用户权限分组返回所有用户 并显示目标类型权限授权情况
@case_api.route('/UserByGroup', methods=['GET'])
@login_required
def users_by_group():
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
                user.hide('active','admin','group_id','update_time','create_time')
            setattr(user_group, 'users', users)
            user_group._fields.append('users')
        else:
            user_groups.remove(user_group)

    return jsonify(user_groups)