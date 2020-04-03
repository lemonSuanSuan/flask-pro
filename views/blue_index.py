#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session, g, Blueprint
from config import Dev
from models import User, Question, Comment
from exts import db
from decorators import login_required
from my_marshmallow import ma
from message import msg_not_enough
from sqlalchemy import or_  # or_即逻辑运算的或
from flask import _request_ctx_stack
# 实例化蓝图对象
blue_index = Blueprint('blue_index', __name__)


# restful 規範，就是前後端分離的做法，返回json數據而不是渲染模板
# 首页
@blue_index.route('/')
def index():

    # # 查询结果根据创建时间进行降序排序，即新的数据排在前面
    questions = Question.query.order_by(Question.create_time.desc()).all()
    # question_schema = QuestionSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    # output = question_schema.dump(questions)  # 生成可序列化对象
    # return jsonify({'data': output})
    # return current_app.send_static_file('test.html')
    return render_template('index.html', data=questions)


# 搜索
@blue_index.route('/search/')
def search():

    q = request.args.get('q')
    # 找到标题或者具体描述含有查询关键字的结果
    results = Question.query.filter(or_(Question.title.contains(q), Question.desc.contains(q)))
    # 将获得的结果重新渲染到index.html
    return render_template('index.html', data=results)
