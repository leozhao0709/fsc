# -*- coding: utf-8 -*-
import logging

import os
from flask_script import Command

__author__ = 'lzhao'
__date__ = '5/15/16'
__time__ = '11:54 AM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# logging.disable(logging.CRITICAL)

class Crawl(Command):
	def run(self):
		print "start Crawl"
		os.system("scrapy crawl nasdaq")
