# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from models.stocks import Stock, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime


class StockPipeline(object):
	def __init__(self):
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.logfile = open('nasdaqpipe.log', 'w')

	def process_item(self, item, spider):
		stock = self.session.query(Stock).filter_by(name=item['name']).first()
		if stock is None:
			stock = Stock(name=item['name'][0], company=item['company'][0], country=item['country'][0],
						  ipoyear=item['ipoyear'][0],
						  description=item['description'][0], yearlowprice=item['yearlowprice'],
						  yearhighprice=item['yearhighprice'], currentprice=item['currentprice'][0])
			try:
				self.session.add(stock)
				self.session.commit()
			except Exception as e:
				now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.logfile.write(
					"{now} find exception {exception} when add new item {item}, company {company}, country {country}, ipoyear {ipoyear}, description {description}, yearlowprice {yearlowprice}, yearhighprice {yearhighprice}, failed url is {url} \n".format(
						now=now, item=item['name'], company=item['company'], country=item['country'],
						ipoyear=item['ipoyear'], description=item['description'], yearlowprice=item['yearlowprice'],
						yearhighprice=item['yearhighprice'],
						url=item['failedurl'], exception=e))
				self.session.rollback()
		else:
			stock.yearlowprice = item['yearlowprice']
			stock.yearhighprice = item['yearhighprice']
			stock.currentprice = item['currentprice'][0]
			try:
				self.session.add(stock)
				self.session.commit()
			except Exception as e:
				now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self.logfile.write(
					"{now} find exception {exception} when change alreay existing item {item}, company {company}, country {country}, ipoyear {ipoyear}, description {description}, yearlowprice {yearlowprice}, yearhighprice {yearhighprice}, failed url is {url} \n".format(
						now=now, item=item['name'], company=item['company'], country=item['country'],
						ipoyear=item['ipoyear'], description=item['description'], yearlowprice=item['yearlowprice'],
						yearhighprice=item['yearhighprice'],
						url=item['failedurl'], exception=e))
				self.session.rollback()

		return item

	def close_spider(self, spider):
		self.logfile.close()
		self.session.close()
