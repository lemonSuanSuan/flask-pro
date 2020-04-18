#!/usr/bin/env python
# -*- coding:utf-8 -*-

# !/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, session, g

from App.middleware import load_middleware
from settings import envs
from App.models import User
from App.exts import init_exts
from App.views import init_views



# 定义一个方法用于创建app
def create_app():
    # 实例化Flask对象
    # 注意，模板和静态文件的路径默认情况下是取Flask实例化的文件路径下的，这里是放在了同一路径下，所以不用修改向相应参数。
    app = Flask(__name__)
    # 加载app配置
    app.config.from_object(envs.get('development'))
    # print('*' * 30)
    # print(app.config)
    # print('*' * 30)
    # 调用自己写的函数init_exts(app)初始化第三方库
    init_exts(app)
    # 调用自己写的函数init_views(app)，在app中注册蓝图
    init_views(app)
    # 中間件（鉤子函數）
    load_middleware(app)


    # 记得要返回app
    return app
