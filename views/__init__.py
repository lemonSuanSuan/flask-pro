#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session, g
from config import Dev
from models import User, Question, Comment
from exts import db
from decorators import login_required
from my_marshmallow import ma
from message import msg_not_enough
from sqlalchemy import or_  # or_即逻辑运算的或

from views.blue_account import blue_account
from views.blue_question import blue_question
from views.blue_index import blue_index
# 实例化Flask对象
# 注意，模板和静态文件的路径默认情况下是取Flask实例化的文件路径下的
# 现在在这里实例化与模板、静态文件不在同一路径，而在上一级目录下，所以要指明到是上级目录的templates和static文件夹
app = Flask(__name__, template_folder='../templates', static_folder='../static')
# 加载app配置
app.config.from_object(Dev)
# 关联db和app，初始化
db.init_app(app)
# 关联ma和app，初始化
ma.init_app(app)

# 在app中注册蓝图
app.register_blueprint(blue_account)
app.register_blueprint(blue_question)
app.register_blueprint(blue_index)


# 钩子函数@app.before_request,每次请求之前都会执行
# 因为question 和comment视图函数都需要通过session找到当前用户id然后找到当前用户对象，代码重复
# 所以在这个钩子函数里把它添加到g对象中（flask中的全局对象）
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


# 钩子函数：上下文处理器。必须返回一个字典，为空也要返回{}
# 上下文处理器返回的字典在所有页面可用
@app.context_processor
def my_context():
    # 在这个钩子函数里判断用户是否已登录，已登录则返回这个用户，这样在每个模板(即html页面)上都可以直接用
    # session['user_id']这种取值方式在没有值的时候会抛出异常，所以用session.get('user_id')这种方式来获取值
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            print('*' * 30)
            print(user.id)
            return {'current_user': user}
    else:
        return {}
