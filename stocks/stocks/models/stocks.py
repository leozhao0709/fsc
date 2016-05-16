# -*- coding: utf-8 -*-
import logging

import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

__author__ = 'lzhao'
__date__ = '5/15/16'
__time__ = '12:21 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# logging.disable(logging.CRITICAL)

# import sqlalchemy
# print sqlalchemy.__version__

engine = create_engine("mysql://{user}:{password}@{host}/fsv".format(
	user=os.environ.get("DB_USER"),
	password=os.environ.get("DB_PASS"), host=os.environ.get("DB_HOST")))

Base = declarative_base()

# Session = sessionmaker(bind=engine)
# session = Session()


class Stock(Base):
	__tablename__ = 'stocks'

	id = Column(Integer, primary_key=True)
	name = Column(String(64), unique=True)
	company = Column(String(64), unique=True)
	country = Column(String(64))
	ipoyear = Column(Integer, nullable=True)
	description = Column(String(64))
	yearlowprice = Column(Float, nullable=True)
	yearhighprice = Column(Float, nullable=True)

	def __repr__(self):
		return '<Stock %r>' % self.name
