#!/usr/bin/env python
# -*- coding:utf-8 -*-

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)  # nullable=False指不能为空
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # 密码密文保存
    # 通过构造函数,在创建模型的时候将其保存为密文
    def __init__(self, *args, **kwargs):
        telephone = kwargs.get('telephone')
        username = kwargs.get('username')
        password = kwargs.get('password')
        self.telephone = telephone
        self.username = username
        self.password = generate_password_hash(password)

    # 定义一个方法，用于登录时将密文密码与输入的密码进行对比，看是否相等
    def check_password(self, raw_password):
        # check_password_hash() 参数1：hash加密后的密码，参数2：输入的密码
        result = check_password_hash(self.password, raw_password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    # 注意是：datetime.now。now是每次创建一个模型的时候都获取当前时间，now()是服务器第一次运行的时间
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 使用外键,db.ForeignKey('user.id')指定外键用到的是user表的id字段
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 建立关系屬性,参数1表示要引用的模型，参数2指定反转时要用到的属性，就是User模型通过哪个属性来获取当前用户发布的所有问题
    author = db.relationship('User', backref=db.backref('questions'))


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键1
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    # 外键2
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # 参数order_by = create_time.desc()表示获取question对应的comments时是按时间倒序的
    question = db.relationship('Question', backref=db.backref('comments', order_by=create_time.desc()))
    author = db.relationship('User', backref=db.backref('comments'))
