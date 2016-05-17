#!/usr/bin/env python
# -*-coding:utf-8-*-
#启动脚本
import os

from app.__init__ import create_app, db
from app.models import User, Role

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app = app,
                db = db,
                User = User,
                Role = Role)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """运行单元测试"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def list_routes():
    import urllib
    links = []
    from flask import url_for
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        links.append(line)
    for line in links:
        print line

if __name__ == '__main__':
    manager.run()


