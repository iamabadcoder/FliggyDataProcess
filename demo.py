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


# def flat_ctrip_data(data_line):
# 	split_fields = data_line.split(',,,,')
# 	city_name = ''
# 	city_link = ''
# 	science_list = '[]'
# 	for i in range(len(split_fields)):
# 		if i == 0:
# 			city_name = split_fields[i].strip()
# 		elif i == 1:
# 			city_link = split_fields[i].strip()
# 		elif i == 2:
# 			science_list = split_fields[i].strip()
# 	for area_info in json.loads(science_list):
# 		sightName = ''
# 		sightUrl = ''
# 		brightSpot = ''
# 		if 'sightName' in area_info:
# 			sightName = area_info['sightName'].strip()
# 		if 'sightUrl' in area_info:
# 			sightUrl = area_info['sightUrl'].strip()
# 		if 'brightSpot' in area_info:
# 			brightSpot = area_info['brightSpot'].strip()
# 		if len(brightSpot) > 2:
# 			content = city_name + '\t' + sightName + '\t' + brightSpot.replace('•', '') + '\n'
# 			write2file(ctrip_scenic_bright_result, content)


# def flat_ctrip_data(data_line):
# 	for link in json.loads(data_line):
# 		print 'sightLink:' + "'" + link + "'"
# 			# content = city_name + '\t' + scenic_name + '\t' + bright_spot + '\n'
# 			# write2file(ctrip_scenic_desc_step1, content)

if __name__ == '__main__':
	# ctrip_scenic_bright = 'ctrip_scenic_bright.txt'
	ctrip_scenic_bright_result = 'ctrip_scenic_bright_result.txt'
	ctrip_scenic_desc_step1 = 'ctrip_scenic_desc_step1.txt'
	ctrip_scenic_bright_final = 'ctrip_scenic_bright_final.txt'

	key_list = []
	for i in range(1, len(open(ctrip_scenic_bright_result, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_scenic_bright_result, i)
		split_fields = line.split('\t')
		city_name = split_fields[0].strip()
		sight_name = split_fields[1].strip()
		key = city_name + sight_name
		if key not in key_list:
			key_list.append(key)
			write2file(ctrip_scenic_bright_final, line)

	for i in range(1, len(open(ctrip_scenic_desc_step1, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_scenic_desc_step1, i)
		split_fields = line.split('\t')
		city_name = split_fields[0].strip()
		sight_name = split_fields[1].strip()
		bright_spot = split_fields[2].strip()
		key = city_name + sight_name
		if key not in key_list:
			key_list.append(key)
			content = city_name + '\t' + sight_name + '\t' + bright_spot.replace('•', '') + '\n'
			write2file(ctrip_scenic_bright_final, content)


	# for i in range(1, len(open(ctrip_scenic_bright, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_scenic_bright, i)
	# 	flat_ctrip_data(line)
	# ctrip_scenic_desc = 'a.txt'
	# ctrip_scenic_desc_step1 = 'aa.txt'
	# for i in range(1, len(open(ctrip_scenic_desc, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_scenic_desc, i)
	# 	flat_ctrip_data(line)
