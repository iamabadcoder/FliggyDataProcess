# -*- coding:utf-8 -*-

import re
import sys
import json
import linecache
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_ctrip_data(data_line):
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
		if area_ratio == '0%':
			area_ratio = '2%'
		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k.strip() == area_name:
					for hotel_item in v:
						hotel_fields = hotel_item.split('######')
						hotel_id = hotel_fields[0].strip()
						hotel_name = hotel_fields[1].strip()
						content = city_name + '####' + city_link + '####' + area_name + '####' + area_ratio + '####'
						content = content + hotel_id + '####' + hotel_name + '\n'
					# write2file(ctrip_area_step_1, content)
					break


if __name__ == '__main__':
	ctrip_area_original = 'ctrip_area_original.txt'
	ctrip_area_step_1 = 'ctrip_area_step_1.txt'
	# for i in range(1, len(open(ctrip_area_original, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_area_original, i)
	# 	flat_ctrip_data(line)

	ctrip_area_step_2 = 'ctrip_area_step_2.txt'
	ctrip_area_step_3 = 'ctrip_area_step_3.txt'
	for i in range(1, len(open(ctrip_area_step_2, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_area_step_2, i)
		split_fields = line.split(',')
		for i in range(len(split_fields)):
			if i == 0:
				c_city_name = split_fields[i].strip()
			elif i == 1:
				c_area_name = split_fields[i].strip()
			elif i == 2:
				c_ratio = split_fields[i].strip()
			elif i == 3:
				f_area_info = split_fields[i].strip()
		unsorted_area = {}
		area_items = f_area_info.split('####')
		for j in range(len(area_items)):
			if area_items[j] not in unsorted_area:
				unsorted_area[area_items[j]] = 1
			else:
				unsorted_area[area_items[j]] += 1

		sorted_areas = sorted(unsorted_area, key=unsorted_area.get, reverse=True)
		matched_f_areas = None
		if len(sorted_areas) >= 1:
			matched_f_areas = sorted_areas[0]
		# if len(sorted_areas) >= 6:
		# 	matched_f_areas = sorted_areas[0] + '####' + sorted_areas[1] + '####' + sorted_areas[2]
		# elif len(sorted_areas) < 2:
		# 	matched_f_areas = sorted_areas[0]
		# else:
		# 	matched_f_areas = sorted_areas[0] + '####' + sorted_areas[1]
		if matched_f_areas is not None:
			content = c_city_name + '\t' + c_area_name + '\t' + c_ratio + '\t'
			content = content + str(20) + '\t' + str(unsorted_area[matched_f_areas]) + '\t' + matched_f_areas
			print content
			# write2file(ctrip_area_step_3, content)

			# content = c_city_name + '\t' + c_area_name + '\t' + c_ratio + '\t' + matched_f_areas + '\n'
			# write2file(ctrip_area_step_3, content)
