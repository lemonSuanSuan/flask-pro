#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
from datetime import timedelta
from redis import Redis


# 基本配置
class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # 设置SECRET_KEY(用到session的话需要设置)
    SECRET_KEY = os.urandom(24)
    # 为了避免中文乱码
    JSON_AS_ASCII = False
    # 指定session类型为redis(使用第三方扩展flask-session需要设置这个)
    SESSION_TYPE = 'redis'
    # 指定缓存存到redis中(为第三方软件flask-cache配置)
    CACHE_TYPE = 'redis'


# 开发环境配置
class DevelopConfig(BaseConfig):
    # 开启修改代码自动重启模式
    DEBUG = True
    # 设置静态文件缓存过期时间(解决静态css修改无法实时更新的问题)
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # session保存数据到redis时启用的链接对象（如果redis没有设置密码，端口号也一致是6379，则可不写以下这条配置）
    # 因为ctrl+B进入Redis代码可以看到连接对象默认端主机就是localhost，默认端口是6379
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379, password='123456')  # 用于连接redis的配置
    # 缓存对应的redis服务器连接
    CACHE_REDIS_HOST = '127.0.0.1'  # redis地址
    CACHE_REDIS_PORT = 6379  # redis端口
    CACHE_REDIS_PASSWORD = '123456'  # redis密码

    # 连接数据库的参数
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'FLASK'
    USERNAME = 'root'
    PASSWORD = '123456'
    # 连接数据库uri: 数据库+驱动://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    # 动态追踪对象修改(可设可不设，根据自己意愿就好)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 显示原生的sql语句
    SQLALCHEMY_ECHO = True


# 测试环境配置
class TestingConfig(BaseConfig):
    TESTING = True
    # 设置静态文件缓存过期时间(解决静态css修改无法实时更新的问题)
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # 连接数据库的参数
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'FLASK'
    USERNAME = 'root'
    PASSWORD = '123456'
    # 连接数据库uri: 数据库+驱动://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379, password='123456')


# 生产环境配置
class ProductConfig(BaseConfig):
    # 连接数据库的参数
    HOST = '127.0.0.1'
    PORT = 3306
    DATABASE = 'FLASK'
    USERNAME = 'root'
    PASSWORD = '123456'
    # 连接数据库uri: 数据库+驱动://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOST, PORT,
                                                                                      DATABASE)
    SESSION_REDIS = Redis(host='127.0.0.1', port=6379, password='123456')


envs = {
    "development": DevelopConfig,
    "testing": TestingConfig,
    "production": ProductConfig
}
