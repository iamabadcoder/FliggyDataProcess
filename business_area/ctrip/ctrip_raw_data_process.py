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


def flat_ctrip_raw_data(data_line, output_file):
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
		business_area_link = business_area_info['businessAreaLink']
		business_area_name = business_area_info['businessAreaName']
		business_area_ratio = business_area_info['businessAreaRatio']
		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k in business_area_name:
					content = city_name + '\t' + city_link + '\t' + business_area_name + '\t'
					content = content + business_area_ratio + '\t' + '####'.join(v) + '\n'
					write2file(output_file, content)


# 将JSON数据转换成二维表形式
def process_step1(input_file, output_file):
	for i in range(1, len(open(input_file, "rU").readlines()) + 1):
		line = linecache.getline(input_file, i)
		flat_ctrip_raw_data(line, output_file)


if __name__ == '__main__':
	ctrip_raw_data_file = './ctrip_business_area_data'
	ctrip_step1_data_file = './ctrip_step1_data_file'

	# process_step1(ctrip_raw_data_file, ctrip_step1_data_file)



