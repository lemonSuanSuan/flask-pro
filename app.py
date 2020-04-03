#!/usr/bin/env python
# -*- coding:utf-8 -*-

from views import app



if __name__ == '__main__':
    app.run()  # 进入方法可以看到threaded=True,即默认开启多线程，每个请求过来都创建一个新的线程来执行
