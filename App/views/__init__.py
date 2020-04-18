#!/usr/bin/env python
# -*- coding:utf-8 -*-


from .blue_account import blue_account
from .blue_index import blue_index
from .blue_question import blue_question
from .blue_utils import blue_utils


# 定义一个方法来注册蓝图，定义在这里视为了能清晰一点，不用全部都放在定义app的文件里，在那里调用这个方法就行
def init_views(app):
    app.register_blueprint(blue_account)
    app.register_blueprint(blue_question)
    app.register_blueprint(blue_index)
    app.register_blueprint(blue_utils)


