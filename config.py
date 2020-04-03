#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
from datetime import timedelta


# 开发环境配置
class Dev(object):
    # 开启修改代码自动重启模式
    DEBUG = True
    # 设置静态文件缓存过期时间(解决静态css修改无法实时更新的问题)
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # 设置SECRET_KEY(用到session的话需要设置)
    SECRET_KEY = os.urandom(24)
    # 连接数据库
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'FLASK'
    USERNAME = 'root'
    PASSWORD = '123456'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    # 动态追踪修改设置(可设可不设，根据自己意愿就好)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 显示原生的sql语句
    SQLALCHEMY_ECHO = True
    # 为了避免中文乱码
    JSON_AS_ASCII = False


# 生产环境配置
class Pro(object):
    pass
