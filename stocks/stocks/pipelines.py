# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from models.stocks import Stock, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class StockPipeline(object):
	def __init__(self):
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.logfile = open('nasdaqpipe.log', 'w')

	def process_item(self, item, spider):
		stock = self.session.query(Stock).filter_by(name=item['name'])
		if stock.count() == 0:
			stock = Stock(name=item['name'], company=item['company'], country=item['country'], ipoyear=item['ipoyear'],
						  description=item['description'], yearlowprice=item['yearlowprice'],
						  yearhighprice=item['yearhighprice'])
		else:
			stock.yearlowprice = item['yearlowprice']
			stock.yearhighprice = item['yearhighprice']
		try:
			self.session.add(stock)
			self.session.commit()
		except:
			now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.logfile.write("{now} find error when store {item} \n".format(now=now, item=item['name'][0]))
			self.session.rollback()
		return item

	def close_spider(self, spider):
		self.logfile.close()
		self.session.close()
