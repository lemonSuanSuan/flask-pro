#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import User,Question,Comment     #导入模型，MigrateCommand就会自动去读取

manager = Manager(app)

migrate = Migrate(app, db)
# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
