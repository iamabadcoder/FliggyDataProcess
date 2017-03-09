# -*- coding:utf-8 -*-

import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_ctrip_raw_data(data_line):
	split_fields = data_line.split(',,,,,')
	for i in range(len(split_fields)):
		if i == 0:
			city_name = split_fields[i].strip()
		elif i == 1:
			city_link = split_fields[i].strip()
		elif i == 2:
			area_info_list = split_fields[i].strip()
		elif i == 3:
			hotel_info_list = split_fields[i].strip()

	for area_info in json.loads(area_info_list):
		area_link = area_info['businessAreaLink'].strip()
		area_name = area_info['businessAreaName'].strip()
		area_ratio = area_info['businessAreaRatio'].strip()
		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k.strip() == area_name:
					content = city_name + '\t' + city_link + '\t' + area_name + '\t'
					content = content + area_ratio + '\t' + '####'.join(v) + '\n'
					write2file(ctrip_area_data_step_1, content)


# 将JSON数据转换成二维表形式
def process_step1(input_file):
	for i in range(1, len(open(input_file, "rU").readlines()) + 1):
		line = linecache.getline(input_file, i)
		flat_ctrip_raw_data(line)


def init_fliggy_areas_by_city_name_key(file_path):
	init_fliggy_areas = {}
	for i in range(1, len(open(file_path, "rU").readlines()) + 1):
		line = linecache.getline(file_path, i)
		f_split_fields = line.split('\t')
		city_name = f_split_fields[3].strip()
		if city_name not in init_fliggy_areas:
			init_fliggy_areas[city_name] = line.strip()
		else:
			init_fliggy_areas[city_name] = init_fliggy_areas[city_name] + '#####BB#####' + line.strip()
	return init_fliggy_areas


if __name__ == '__main__':
	ctrip_area_data_original = 'ctrip_area_data_original.txt'
	fliggy_area_data_original = 'fliggy_area_data_original.txt'
	ctrip_area_data_step_1 = 'ctrip_area_data_step_1.txt'
	ctrip_area_data_step_2 = 'ctrip_area_data_step_2.txt'

	init_fliggy_areas = init_fliggy_areas_by_city_name_key(fliggy_area_data_original)

	for i in range(1, 802):
		print i
		line = linecache.getline(ctrip_area_data_step_1, i)
		ctrip_split_fields = line.split('\t')
		for i in range(len(ctrip_split_fields)):
			if i == 0:
				c_city_name = ctrip_split_fields[i].strip()
			elif i == 1:
				c_city_link = ctrip_split_fields[i].strip()
			elif i == 2:
				c_area_name = ctrip_split_fields[i].strip()
			elif i == 3:
				c_area_ratio = ctrip_split_fields[i].strip()
			elif i == 4:
				c_hotel_list = ctrip_split_fields[i].strip().split('####')

		matched_hotels = {}
		matched_hotels_detail = {}
		if c_city_name in init_fliggy_areas:
			for zone_line in init_fliggy_areas[hq_city_name].split('#####BB#####'):
				f_split_fields = zone_line.split('\t')
				f_area_id = f_split_fields[0].strip()
				f_area_name = f_split_fields[1].strip()
				f_hotel_list = f_split_fields[4].strip().split('####')
				matched_count, matched_list = match_hotels(hq_hotel_list, f_hotel_list, hq_city_name)
				if matched_count / len(hq_hotel_list) >= 0.5:
					matched_hotels[f_area_id + '@@@@' + f_area_name] = matched_count
					matched_hotels_detail[f_area_id + '@@@@' + f_area_name] = matched_list

			sorted_matched_hotels = sorted(matched_hotels, key=matched_hotels.get, reverse=True)