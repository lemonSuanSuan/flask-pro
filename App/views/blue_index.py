#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import render_template, request, Blueprint, jsonify, g

from App.exts import cache
from App.models import Question
from sqlalchemy import or_  # or_即逻辑运算的或


# 实例化蓝图对象
blue_index = Blueprint('blue_index', __name__)


# restful 規範，就是前後端分離的做法，返回json數據而不是渲染模板
# 首页
@blue_index.route('/')
def index():
    cache.set("test",1)
    page = request.args.get('page', 1, type=int)  # 设定page参数默认值为1，类型为整型
    per_page = request.args.get('per_page', 4, type=int)
    # 分页实现
    # 方法1：offset为偏移量，limit限制返回的记录数
    # questions = Question.query.order_by(Question.create_time.desc()).offset(per_page*(page-1)).limit(per_page)

    # 方法2：使用paginate，这样可通过paginate.pages获取总页数而不需要自己再另外计算
    paginate = Question.query.order_by(Question.create_time.desc()).paginate(page, per_page, error_out=False)
    # questions = paginate.items  # 获取当前页数据
    print("总页数:{}".format(paginate.pages)) # 总页数
    return render_template('index.html', paginate=paginate, per_page=per_page)


# 搜索
@blue_index.route('/search/')
def search():
    page = request.args.get('page', 1, type=int)  # 设定page参数默认值为1，类型为整型
    per_page = request.args.get('per_page', 4, type=int)
    q = request.args.get('q')
    # 找到标题或者具体描述含有查询关键字的结果
    paginate = Question.query.filter(or_(Question.title.contains(q), Question.desc.contains(q))).\
        paginate(page, per_page, error_out=False)
    # 将获得的结果重新渲染到index.html
    return render_template('index.html', paginate=paginate, per_page=per_page)
