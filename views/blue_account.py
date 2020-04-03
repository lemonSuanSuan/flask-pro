#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session, g, Blueprint
from config import Dev
from models import User, Question, Comment
from exts import db
from decorators import login_required
from my_marshmallow import ma
from message import msg_not_enough, msg_ok
from sqlalchemy import or_  # or_即逻辑运算的或

# 实例化蓝图对象
blue_account = Blueprint('blue_account', __name__)


# 注册
@blue_account.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password2')
        # 验证表单
        if not all([telephone, username, password, password1]):
            response = {'msg': msg_not_enough}
            return jsonify(response)
        else:
            user = User.query.filter(User.telephone == telephone).first()
            if user:
                return jsonify({'msg': '该号码已被注册过'})
            else:
                if password != password1:
                    return jsonify({'msg': '两次密码不相等，请核对后输入'})
                else:
                    user = User(telephone=telephone, username=username, password=password)
                    # 添加数据到数据库
                    db.session.add(user)
                    db.session.commit()
                    return jsonify({'msg': msg_ok})


# 登录
@blue_account.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        if not all([telephone, password]):
            return jsonify({'msg': msg_not_enough})
        else:
            user = User.query.filter(User.telephone == telephone).first()
            if user and user.check_password(password):
                # 设置session
                session['user_id'] = user.id
                # 31天内不需要重新登录
                session.permanent = True
                return jsonify({'msg': msg_ok})
            else:
                return jsonify({'msg': '请输入正确手机号和密码'})


# 退出登录，删除作为登录认证的session字段即可
@blue_account.route('/logout/')
def logout():
    # 以下三个语法都可以
    # session.pop('user_id')
    del session['user_id']
    # session.clear()   # 这个是把session全部清除,适用于当session只有user_id时
    return redirect(url_for('login'))
