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


def init_city_id_name_map(in_file):
	city_id_name_map = {}
	for i_line_num in range(1, len(open(in_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(in_file, i_line_num)
		split_fields = i_line.split('\t')
		city_id_name_map[unicode(split_fields[1].strip())] = split_fields[0].strip()
	return city_id_name_map


def flat_accommodation_info(in_file, out_file):
	# 初始化城市ID和名称的MAP
	city_id_name_map = init_city_id_name_map(file_city_id_name_mapping)

	pattern = re.compile(u'若以(.*?)[作]?为考量')
	for i_line_num in range(1, len(open(in_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(in_file, i_line_num)
		json_obj = json.loads(i_line)
		destination = json_obj['destination']
		accommodation_info = json_obj['accommodation_info']
		for info in accommodation_info.split('\n'):
			judge = '概述'
			city_code = 'CITY_CODE'
			m = pattern.search(info)
			if m is not None:
				judge = m.group(1)
			if destination in city_id_name_map.keys():
				city_code = city_id_name_map[destination]
			content = city_code + '-->' + destination + '-->' + judge + '-->' + info + '\n'
			write2file(out_file, content)


def init_business_info_map(in_file):
	business_info_map = {}
	for i_line_num in range(1, len(open(in_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(in_file, i_line_num)
		split_fields = i_line.split('\t')
		business_id = split_fields[0]
		business_name = split_fields[1]
		province_id = split_fields[2]
		city_id = split_fields[3]
		business_name_en = split_fields[4]

		if city_id not in business_info_map.keys():
			business_list = []
		else:
			business_list = business_info_map[city_id]
		business_dict = {}
		business_dict['id'] = business_id
		business_dict['cn_name'] = business_name
		business_dict['en_name'] = business_name_en
		business_list.append(business_dict)
		business_info_map[city_id] = business_list
	return business_info_map


def match_business(in_file, out_file):
	# 初始化城市ID和名称的MAP
	business_info_map = init_business_info_map(file_hotel_business_area)

	for i_line_num in range(1, len(open(in_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(in_file, i_line_num)
		if 'CITY_CODE' in i_line: continue
		split_fields = i_line.split('-->')
		city_id = split_fields[0].strip()
		accommodation_desc = split_fields[3].strip()
		relate_business = []
		if city_id in business_info_map.keys():
			for business_info in business_info_map[city_id]:
				business_id = business_info['id']
				business_ch_name = business_info['cn_name']
				business_en_name = business_info['en_name']
				if business_ch_name in accommodation_desc:
					relate_business.append(business_ch_name)
				elif business_en_name in accommodation_desc:
					relate_business.append(business_en_name)
		if len(relate_business) > 0:
			i_line = i_line.strip() + '-->' + '@@@@'.join(relate_business) + '\n'
		else:
			i_line = i_line.strip() + '-->' + '' + '\n'
		write2file(out_file, i_line)


if __name__ == '__main__':
	file_match_step_1 = 'match_step_1.txt'
	file_match_step_2 = 'match_step_2.txt'
	file_accommodation_info = 'accommodation_info.txt'
	file_city_id_name_mapping = 'city_id_name_mapping.txt'
	file_hotel_business_area = 'hotel_business_area.txt'

	# flat_accommodation_info(file_accommodation_info, file_match_step_1)
	match_business(file_match_step_1, file_match_step_2)
