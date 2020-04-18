#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import render_template, request, url_for, redirect, jsonify, session, Blueprint, flash, abort
from App.models import User
from App.exts import db, cache

# 实例化蓝图对象
blue_account = Blueprint('blue_account', __name__)


# 注册
@blue_account.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        code = request.form.get('code')
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password2')
        # 验证表单
        if not all([telephone, username, password, password1]):
            flash('参数不足')
            return redirect(url_for('blue_account.register'))
        else:
            user = User.query.filter(User.telephone == telephone).first()
            if user:
                flash('该号码已被注册过')
                return redirect(url_for('blue_account.register'))
            elif password != password1:
                flash('两次密码不相等，请核对后输入')
                return redirect(url_for('blue_account.register'))
            else:
                # 缓存中获取验证码
                cache_code = cache.get(telephone)
                print(type(code))
                print(type(cache_code))
                # 如果用户输入的验证码与缓存中的验证码不相等，返回验证失败给前端
                if code != cache_code:
                    return '验证失败'
                user = User(telephone=telephone, username=username, password=password)
                # 添加数据到数据库
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('blue_account.login'))


# 登录
@blue_account.route('/login/', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        remember = request.form.get('remember')
        if not all([telephone, password]):
            flash('参数不足')
            return redirect(url_for('blue_account.login'))
        else:
            user = User.query.filter(User.telephone == telephone).first()
            if user and user.check_password(password):
                # 设置session
                session['user_id'] = user.id
                # if not remember:
                #     # 勾选了记住密码，则设置session.permanent为True,这样会在31天后过期
                #     session.permanent = False
                return redirect(url_for('blue_index.index'))
            else:
                flash('请输入正确手机号和密码')
                return redirect(url_for('blue_account.login'))


# 退出登录，删除作为登录认证的session字段即可
@blue_account.route('/logout/')
def logout():
    # 以下三个语法都可以
    session.pop('user_id')
    # del session['user_id']
    # session.clear()   # 这个是把session全部清除,适用于当session只有user_id时
    return redirect(url_for('blue_account.login'))
