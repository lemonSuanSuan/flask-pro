#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from App import create_app



# 调用自己写的函数create_app()创建app
app = create_app()



manager = Manager(app)
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
