#!/usr/bin/env python
#-*- coding:utf-8 -*-

from flask import render_template, request, url_for, redirect, jsonify, flash, g,Blueprint
from App.models import Question, Comment
from App.exts import db
from decorators import login_required


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
            flash('参数不足')
            return redirect(url_for('blue_question.question'))
        else:
            question_rel = Question(title=title, desc=desc)
            # 将当前用户賦值给关系属性author
            question_rel.author = g.user
            db.session.add(question_rel)
            db.session.commit()
            return redirect(url_for('blue_index.index'))



# 详情页
@blue_question.route('/detail/<int:question_id>')
@login_required  # 自己写的装饰器
def detail(question_id):
    q = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=q)


# 添加评论
@blue_question.route('/add_comment/', methods=['POST','PUT','PATCH'])
@login_required  # 自己写的装饰器
def add_comment():
    print("获得参数了吗")
    print(request.args)
    content = request.form.get('content')
    question_id = request.form.get('question_id')
    if not all([content, question_id]):
        flash('请输入内容 ')
        return redirect(url_for('blue_question.detail', question_id=question_id))
    else:
        comment = Comment(content=content)
        comment.author = g.user
        belong_question = Question.query.filter(Question.id == question_id).first()
        comment.question = belong_question
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blue_question.detail', question_id=question_id))