# -*- coding: utf-8 -*-
import logging

__author__ = 'lzhao'
__date__ = '5/15/16'
__time__ = '8:05 PM'

logging.basicConfig(filename=None, level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


# logging.disable(logging.CRITICAL)

def filter_number(value):
	if value.isdigit():
		return value
	else:
		return 0
