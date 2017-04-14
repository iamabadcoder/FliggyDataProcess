# -*- coding:utf-8 -*-

import os
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_region_accommodation_strategy(input_file):
	for i_line_num in range(1, len(open(input_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(input_file, i_line_num)
		split_fields = i_line.split(',,,,,')
		city_name = split_fields[0]
		region_info_obj = json.loads(split_fields[2])
		for region in region_info_obj:
			region_desc = region['regionDesc']
			region_name = region['regionName']
			content = city_name + '-->' + region_name + '-->' + region_desc + '\n'
			write2file(file_region_accommodation_strategy_formated, content)


if __name__ == '__main__':
	file_region_accommodation_strategy = 'region_accommodation_strategy.txt'
	file_region_accommodation_strategy_formated = 'region_accommodation_strategy_formated.txt'
	flat_region_accommodation_strategy(file_region_accommodation_strategy)
