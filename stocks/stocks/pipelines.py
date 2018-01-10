# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from models.stocks import Stock, engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from scrapy.mail import MailSender
from stocks.emailsettings import emailSettings
from datetime import datetime


class StockPipeline(object):
	def __init__(self):
		Session = sessionmaker(bind=engine)
		self.session = Session()
		self.logfile = open('stockpipeline.txt', 'w')
		self.logfile.write("stock pipeline start \n")
		self.emailContent = {}

	def process_item(self, item, spider):
		stock = self.session.query(Stock).filter_by(name=item['name']).first()
		if stock is None:
			stock = Stock(name=item['name'][0], company=item['company'][0], country=item['country'][0],
						  ipoyear=item['ipoyear'][0],
						  description=item['description'][0], yearlowprice=item['yearlowprice'][0],
						  yearhighprice=item['yearhighprice'][0], currentprice=item['currentprice'][0],
						  sharevolume=item['sharevolume'][0])
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
			stock.yearlowprice = item['yearlowprice'][0]
			stock.yearhighprice = item['yearhighprice'][0]
			stock.currentprice = item['currentprice'][0]
			stock.sharevolume = item['sharevolume'][0]
			stock.updatetime = datetime.now()
			if stock.yearlowprice > stock.currentprice and stock.sharevolume > 100000:
				self.emailContent[item['name'][0]] = [stock.currentprice, stock.yearlowprice, stock.yearhighprice, stock.sharevolume]
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
		self.logfile.write("stock pipeline finish \n")
		pipelog = open("stockpipeline.txt")
		if spider.name == "nasdaq":
			# mail body
			mail_body = "please consider the following {count} stocks: \n".format(count=len(self.emailContent))
			for name, content in self.emailContent.items():
				mail_body += "{name}	{currentprice}	{yearlowprice}	{yearhighprice}	{sharevolume} \n".format(
					name=name, currentprice=content[0], yearlowprice=content[1], yearhighprice=content[2], sharevolume=content[3])

			nasdaqlog = open("nasdaqcrawl.txt")
			attachment = [('nasdaqlog.txt', 'text/plain', nasdaqlog), ('pipelog.txt', 'text/plain', pipelog)]
			mailer = MailSender.from_settings(emailSettings())
			mailer.send(to=["leo.zhao.real@gmail.com"],
						subject='nasdaq spider finish', body=mail_body, cc=["leo.zhao.real@gmail.com"],
						attachs=attachment)
			nasdaqlog.close()
		pipelog.close()
		self.logfile.close()
		self.session.close()
