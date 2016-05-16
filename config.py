# -*- coding: utf-8 -*-
import logging
import os

__author__ = 'lzhao'
__date__ = '5/14/16'
__time__ = '4:43 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

logging.disable(logging.CRITICAL)


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	FLASK_MAIL_SUBJECT_PREFIX = '[FSC]'
	FLASK_MAIL_SENDER = 'FSC'
	FLASK_ADMIN = os.environ.get('MAIL_USERNAME')

	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or "mysql://{user}:{password}@{host}/fsv".format(
		user=os.environ.get("DB_USER"),
		password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST"))


config = {
	'development': DevelopmentConfig,

	'default': DevelopmentConfig
}
