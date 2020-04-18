#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 写一个登录限制装饰器。
# 在需要登录才能访问的页面的试图函数前加上这个函数装饰器即可
from functools import wraps
from flask import session, redirect, url_for


def login_required(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('blue_account.login'))
    return wraper
