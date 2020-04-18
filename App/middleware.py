#!/usr/bin/env python
#-*- coding:utf-8 -*-
from flask import session, g
from App.models import User

def load_middleware(app):
    # 钩子函数@app.before_request,每次请求之前都会执行
    # 因为question 和comment视图函数都需要通过session找到当前用户id然后找到当前用户对象，代码重复
    # 所以在这个钩子函数里把它添加到g对象中（flask中的全局对象）
    @app.before_request
    def my_before_request():
        # session['user_id']这种取值方式在没有值的时候会抛出异常，所以用session.get('user_id')这种方式来获取值
        user_id = session.get('user_id')
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            # 根据主键id查询还可以用User.query.get(),注意这个方法只接受主键作为参数
            # user = User.query.get(user_id)
            if user:
                g.user = user
                print(g.user.username)

    # 钩子函数：上下文处理器。必须返回一个字典，为空也要返回{}
    # 上下文处理器返回的字典在所有页面可用
    @app.context_processor
    def my_context():
        # 在这个钩子函数里判断用户是否已登录，已登录则返回这个用户，这样在每个模板(即html页面)上都可以直接用
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            print("这里的名字是：{}".format(user.username))
            return {'current_user': user.username}
        else:
            return {}

    # # 捕获异常
    # @app.errorhandler(404)
    # def handle_error(error):
    #     print(error)
    #     # 生产环境可以捕获所有404重定向到首页，这样用户体验比较好
    #     return '捕获了404异常'