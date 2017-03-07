# -*- coding:utf-8 -*-

import os
import re
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def extract_ratio(desc):
	pattern = re.compile(r'(\d+%)')
	match = pattern.match(desc)
	if match:
		return match.group(1)
	else:
		return '2%'


def flat_haoqiao_raw_data(data_line):
	split_fields = data_line.split(',,,,,')
	for i in range(len(split_fields)):
		if i == 0:
			city_name = split_fields[i].strip()
		elif i == 1:
			city_link = split_fields[i].strip()
		elif i == 2:
			business_area_info_list = split_fields[i].strip()
		elif i == 3:
			hotel_info_list = split_fields[i].strip()

	for business_area_info in json.loads(business_area_info_list):
		business_area_id = business_area_info['businessAreaId']
		business_area_name = business_area_info['businessAreaTitle']
		if business_area_info.has_key('businessAreaDesc'):
			business_area_desc = business_area_info['businessAreaDesc']
		else:
			business_area_desc = '2%的游客选择住这里，-1家酒店'
		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k.strip() == business_area_name.strip():
					ratio = extract_ratio(business_area_desc)
					content = city_name + '\t' + city_link + '\t' + business_area_name + '\t'
					content = content + ratio + '\t' + '####'.join(v) + '\n'
					write2file(haoqiao_step1_data_file, content)
					break


if __name__ == '__main__':
	haoqiao_raw_data_file = './haoqiao/haoqiao_business_area_data'
	haoqiao_step1_data_file = './haoqiao/haoqiao_step1_data_file'

	# 将JSON数据转换成二维表形式
	for i in range(1, len(open(haoqiao_raw_data_file, "rU").readlines()) + 1):
		line = linecache.getline(haoqiao_raw_data_file, i)
		flat_haoqiao_raw_data(line)
