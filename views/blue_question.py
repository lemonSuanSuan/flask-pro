#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import Flask, render_template, request, url_for, redirect, jsonify, flash, session, g,Blueprint
from config import Dev
from models import User, Question, Comment
from exts import db
from decorators import login_required
from my_marshmallow import ma
from message import msg_not_enough,msg_ok
from sqlalchemy import or_  # or_即逻辑运算的或

# 实例化蓝图对象
blue_question = Blueprint('blue_question', __name__)

# 发布问题
@blue_question.route('/question/', methods=['GET', 'POST'])
@login_required  # 自己写的装饰器
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        desc = request.form.get('desc')
        if not all([title, desc]):
            return jsonify({'msg': msg_not_enough})
        else:
            question_rel = Question(title=title, desc=desc)
            # 将当前用户賦值给关系属性author
            question_rel.author = g.user
            db.session.add(question_rel)
            db.session.commit()
            # 1.restful开发
            # return jsonify({'msg': msg_ok})
            # 2.web开发
            return url_for('index')




# 详情页
@blue_question.route('/detail/<int:question_id>')
@login_required  # 自己写的装饰器
def detail(question_id):
    q = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=q)


# 添加评论
@blue_question.route('/add_comment/', methods=['POST'])
@login_required  # 自己写的装饰器
def add_comment():
    content = request.form.get('content')
    question_id = request.form.get('question_id')
    if not all([content, question_id]):
        flash('请输入内容 ')
        return redirect(url_for('detail',question_id=question_id))
    else:
        comment = Comment(content=content)
        comment.author = g.user
        belong_question = Question.query.filter(Question.id == question_id).first()
        comment.question = belong_question
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('detail', question_id=question_id))