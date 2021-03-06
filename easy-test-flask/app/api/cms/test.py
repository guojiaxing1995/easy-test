"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from time import sleep

from flask_mail import Message
from lin.exception import Success
from lin.redprint import Redprint
from flask import jsonify, request
from lin.jwt import group_required
from lin.core import route_meta

from app.libs.init import mongo, mail

test_api = Redprint('test')


@test_api.route('', methods=['GET'])
def slogan():
    return """<style type="text/css">*{ padding: 0; margin: 0; } div{ padding: 4px 48px;} a{color:#2E5CD5;cursor: 
    pointer;text-decoration: none} a:hover{text-decoration:underline; } body{ background: #fff; font-family: 
    "Century Gothic","Microsoft yahei"; color: #333;font-size:18px;} h1{ font-size: 100px; font-weight: normal; 
    margin-bottom: 12px; } p{ line-height: 1.6em; font-size: 42px }</style><div style="padding: 24px 48px;"><p> 
    Lin <br/><span style="font-size:30px">遇事不决 可问春风</span></p></div> """


@test_api.route('/info', methods=['GET'])
@route_meta(auth='查看lin的信息', module='信息')
# @Logger(template='{user.nickname}浏览了信息')  # 记录日志
@group_required
def info():
    return jsonify({
        'msg': 'Lin 是一套基于 Python-Flask 的一整套开箱即用的后台管理系统（CMS）。Lin 遵循简洁、高效的原则，通过核心库加插件的方式来驱动整个系统高效的运行'
    })


# --------------------------------------------------
# --------------------Test--------------------------
# --------------------------------------------------
# -------------------Abandon------------------------
# @test_api.route('/ac', methods=['GET'])
# @route_meta(auth='用户查询自己信息', module='权限')
# @login_required
# @Logger(template='{user.nickname}查询了自己的名字，状态码为{response.status_code}')
# def get_active():
#     return jsonify({
#         'hello': current_user.active
#     })
#
#
# @test_api.route('/ni', methods=['GET'])
# @route_meta(auth='用户查询自己信息', module='权限')
# @group_required
# @Logger(template='{user.nickname}查询了自己的名字，状态码为{response.status_code}')
# def get_name():
#     return jsonify({
#         'hello': current_user.nickname
#     })


@test_api.route('/mongo', methods=['GET'])
def mongo_test():
    users = mongo.db.easy.find()
    users = list(users)
    for user in users:
        del user['_id']
    return jsonify(users)


@test_api.route('/a/<aid>', methods=['GET'])
def test_a(aid):
    sleep(3)
    return jsonify({
        "name": "小明啊",
        "id": int(aid) + 2
    })


@test_api.route('/b', methods=['POST'])
def test_b():
    sleep(3)
    form = request.form
    age = form['age']
    return jsonify({
        "id": int(age) + 5,
        "time": 'now'
    })


@test_api.route('/c', methods=['PUT'])
def test_c():
    sleep(3)
    form = request.json
    address = form['address']
    return jsonify({
        "address_new": address,
        "age": 10
    }), 205, {}


@test_api.route('/d', methods=['DELETE'])
def test_d():
    sleep(3)
    return jsonify({
        "success": True,
        "msg": 'is ok !'
    })


@test_api.route('/mail', methods=['GET'])
def test_mail():
    msg = Message(
        subject="Hello World!",
        html="<b>testing</b>",
        sender=("自动化测试平台", "15234093915@sina.cn"),
        recipients=["302802003@qq.com"],
        cc=['15234093915@163.com']
    )

    mail.send(msg)
    return Success()
