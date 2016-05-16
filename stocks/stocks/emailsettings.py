# -*- coding: utf-8 -*-
import logging

from scrapy.settings import Settings
from stocks import settings

__author__ = 'lzhao'
__date__ = '5/15/16'
__time__ = '11:14 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# logging.disable(logging.CRITICAL)

class emailSettings(Settings):
	def __init__(self):
		super(emailSettings, self).__init__()
		self.setmodule(settings, priority='default')

