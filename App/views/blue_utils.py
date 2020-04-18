#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint, request, jsonify

from App.exts import cache
from App.utils import send_verify_code

blue_utils = Blueprint('blue_utils', __name__)


@blue_utils.route('/sendcode/')
def send_code():
    telephone = request.args.get('telephone')
    resp = send_verify_code(telephone)
    result = resp.json()
    print(result)
    # 判断是否发送成功
    # 成功则放到缓存中，并发送了则返回200给前端
    if result.get('code') == 200:
        obj = result.get('obj')  # 获取验证码
        cache.set(telephone, obj)  # 将手机号及对应的验证码存储到缓存中
        data = {
            "msg": "ok",
            "status": 200
        }
        return jsonify(data)
    # 不成功则返回400给前端
    data = {
        "msg": "fail",
        "status": 400
    }
    return jsonify(data)
