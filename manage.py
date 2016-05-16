# -*- coding: utf-8 -*-
import logging

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from web.models import stocks
from web import create_app, db
from command.crawl import Crawl

__author__ = 'lzhao'
__date__ = '5/14/16'
__time__ = '5:21 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# logging.disable(logging.CRITICAL)

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
	return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('crawl', Crawl())

if __name__ == '__main__':
	manager.run()
