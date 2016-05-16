# -*- coding: utf-8 -*-
import logging
from web import db

__author__ = 'lzhao'
__date__ = '5/14/16'
__time__ = '6:16 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# logging.disable(logging.CRITICAL)


class Stock(db.Model):
	__tablename__ = 'stocks'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	company = db.Column(db.String(64))
	country = db.Column(db.String(64))
	ipoyear = db.Column(db.Integer, nullable=True)
	description = db.Column(db.String(64))
	yearlowprice = db.Column(db.Float, nullable=True)
	yearhighprice = db.Column(db.Float, nullable=True)

	def __repr__(self):
		return '<Stock %r>' % self.name
