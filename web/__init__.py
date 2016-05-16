# -*- coding: utf-8 -*-
import logging
from flask import Flask
from flask.ext.mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

__author__ = 'lzhao'
__date__ = '5/14/16'
__time__ = '4:58 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# logging.disable(logging.CRITICAL)

mail = Mail()
db = SQLAlchemy()


def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	mail.init_app(app)
	db.init_app(app)

	return app
