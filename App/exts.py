#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 新建exts.py文件用于用于统一管理扩展库
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_caching import Cache
db = SQLAlchemy()
migrate = Migrate()
sess = Session()
cache = Cache()


# 定义一个方法init_exts来初始化第三方库，即绑定其与app
def init_exts(app):
    # 初始化
    db.init_app(app)
    migrate.init_app(app, db)
    sess.init_app(app)
    cache.init_app(app)
