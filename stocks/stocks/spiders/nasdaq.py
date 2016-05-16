# -*- coding: utf-8 -*-
import urlparse
from datetime import datetime

import scrapy
from stocks.items import StockItem
from scrapy.http import Request
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose


class NasdaqSpider(scrapy.Spider):
	handle_httpstatus_list = [404, 500]
	name = "nasdaq"
	allowed_domains = ["nasdaq.com"]
	start_urls = (
		'http://www.nasdaq.com/screening/companies-by-name.aspx/',
	)

	def __init__(self):
		super(NasdaqSpider, self).__init__()
		self.logfile = open('nasdaqcrawl.log', 'w')

	def parse(self, response):
		next_alpha = response.xpath('//*[@id="alpha-list"]/ul//li/a/@href')
		for url in next_alpha.extract():
			yield Request(urlparse.urljoin(response.url, url))

		next_page = response.xpath('//*[@id="main_content_lb_NextPage"]/@href')
		for url in next_page.extract():
			yield Request(url)

		selectors = response.xpath('//*[@id="CompanylistResults"]//tr')
		for selector in selectors:
			url = selector.xpath('./td[2]/h3/a/@href').extract()
			if len(url) != 0:
				name = selector.xpath('./td[2]/h3/a/text()').extract()[0]
				company = selector.xpath('./td[1]//text()').extract()[0]
				country = selector.xpath('./td[5]/text()').extract()[0]
				ipoyear = selector.xpath('./td[6]/text()').extract()[0]
				description = selector.xpath('./td[7]/text()').extract()[0]
				yield Request(unicode.strip(url[0]),
							  meta={'name': name, 'company': company, 'country': country, 'ipoyear': ipoyear,
									'description': description}, callback=self.parse_company)

	def parse_company(self, response):
		if response.status == 404:
			now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			self.logfile.write(
				"{now} find error when store {item}, the url is {url} \n".format(now=now, item=response.meta['name'],
																				 url=response.url))

		l = ItemLoader(item=StockItem(), response=response)
		l.add_value('name', response.meta['name'], MapCompose(unicode.strip))
		l.add_value('company', response.meta['company'], MapCompose(unicode.strip))
		l.add_value('country', response.meta['country'], MapCompose(unicode.strip))
		l.add_value('ipoyear', response.meta['ipoyear'], MapCompose(unicode.strip))
		l.add_value('description', response.meta['description'], MapCompose(unicode.strip))

		# price
		price = response.xpath(
			'//*[@id="52_week_high_low"]/../following-sibling::td/text()').re(
			'[.0-9]+')
		yearhighprice = price[0]
		yearlowprice = price[1]
		l.add_value('yearhighprice', yearhighprice, MapCompose(unicode.strip))
		l.add_value('yearlowprice', yearlowprice, MapCompose(unicode.strip))

		return l.load_item()