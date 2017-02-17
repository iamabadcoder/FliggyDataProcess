# -*- coding:utf-8 -*-

import sys
import json
import uniout
import pypinyin
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_json_data(data_line):
	field_list = data_line.split(',')
	for i in range(len(field_list)):
		if i == 1:
			pass
		elif i == 2:
			pass
		elif i == 3:
			city_name = field_list[i]
		elif i == 4:
			city_link = field_list[i]
		elif i >= 5:
			zone_info = ','.join(field_list[5:len(field_list)])
			break
	for zone in json.loads(zone_info):
		zone_group_ratio = None
		zone_group_name = None
		for key in zone:
			if 'zoneGroupRatio' in key:
				zone_group_ratio = zone['zoneGroupRatio']
			elif 'zoneGroupName' in key:
				zone_group_name = zone['zoneGroupName']
			if zone_group_ratio is not None and zone_group_name is not None:
				write2file(ctrip_setp1_file_name,
						   city_name + '\t' + city_link + '\t' + zone_group_name + '\t' + zone_group_ratio + '\n')


def get_ctrip_cities(file_name):
	l_cities = []
	m_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_name = line.split('\t')[0]
		l_cities.append(city_name)
	# city_url = line.split('\t')[1]
	# if city_name in m_cities:
	# 	if city_url != m_cities.get(city_name):
	# 		print city_name
	# else:
	# 	m_cities[city_name] = city_url
	l_cities = list(set(l_cities))
	# print len(l_cities)
	return l_cities


def get_fliggy_cities(file_name):
	l_cities = []
	m_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_id = line.split('\t')[0]
		city_name = line.split('\t')[2]
		l_cities.append(city_name)
		if city_id not in m_cities:
			m_cities[city_id] = city_name
	l_cities = list(set(l_cities))
	# print len(l_cities)
	# print len(m_cities)
	return l_cities, m_cities


def get_zone_list_from_fliggy(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[2]:
			zone_list.append(field_list[4])
	return zone_list


def get_zone_list_from_fliggy_city_pinyin(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == pypinyin.slug(unicode(field_list[2]), separator=''):
			zone_list.append(field_list[4])
	return zone_list


def get_zone_list_from_ctrip(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[0]:
			print
			zone_list.append(field_list[2])
	return zone_list


if __name__ == '__main__':
	source_file_name = 'ctrip_hotel_guide_data_from_odps.txt'
	ctrip_setp1_file_name = 'ctrip_hotel_guide_data_step1.txt'
	fliggy_setp1_file_name = 'fliggy_zone_data_step1.txt'

	# JSON格式数据扁平化
	# for i in range(1, len(open(source_file_name, "rU").readlines()) + 1):
	# 	line = linecache.getline(source_file_name, i)
	# 	flat_json_data(line)

	# 获取城市名称
	ctrip_cities = get_ctrip_cities(ctrip_setp1_file_name)
	fliggy_cities_list, fliggy_cities_map = get_fliggy_cities(fliggy_setp1_file_name)
	fliggy_cities_pinyin = [pypinyin.slug(unicode(city), separator='') for city in fliggy_cities_list]

	count = 0
	for city in ctrip_cities:
		if city in fliggy_cities_list:
			print str(get_zone_list_from_ctrip(city, ctrip_setp1_file_name)).decode('string_escape')
			print str(get_zone_list_from_fliggy(city, fliggy_setp1_file_name)).decode('string_escape')
		elif pypinyin.slug(unicode(city), separator='') in fliggy_cities_pinyin:
			print str(get_zone_list_from_ctrip(city, ctrip_setp1_file_name)).decode('string_escape')
			print str(get_zone_list_from_fliggy_city_pinyin(pypinyin.slug(unicode(city), separator=''),
															fliggy_setp1_file_name)).decode('string_escape')
		else:
			continue
