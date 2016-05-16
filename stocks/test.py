# -*- coding: utf-8 -*-
import logging

__author__ = 'lzhao'
__date__ = '5/15/16'
__time__ = '1:26 PM'


def main():
	# logging.basicConfig(filename='myapp.log', level=logging.INFO)
	logging.basicConfig(filename="nasdaq.log", filemode='w', level=logging.DEBUG,
						format="%(asctime)s - %(levelname)s - %(message)s")
	logging.info('Started')
	logging.info('Finished')

if __name__ == '__main__':
	main()
