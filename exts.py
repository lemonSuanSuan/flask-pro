#!/usr/bin/env python
# -*- coding:utf-8 -*-


# 为了解决循环引用问题，新建exts.py文件来定义db对象

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


