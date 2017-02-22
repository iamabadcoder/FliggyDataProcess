# -*- coding:utf-8 -*-

import sys
import json
import uniout
import pypinyin
import linecache
import Levenshtein

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_json_data(data_line, file_name):
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
				write2file(file_name,
						   city_name + '\t' + city_link + '\t' + zone_group_name + '\t' + zone_group_ratio + '\n')


def get_ctrip_cities(file_name):
	m_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_name = line.split('\t')[0].strip()
		city_link = line.split('\t')[1].strip()
		if city_name in m_cities:
			if city_link != m_cities[city_name]:
				# 一旦执行到此行，表明城市名称有相同的
				print "ERROR ERROR ERROR"
		else:
			m_cities[city_name] = city_link
	print len(m_cities)
	return m_cities


def get_fliggy_cities(file_name):
	m_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_id = line.split('\t')[0].strip()
		city_name = line.split('\t')[2].strip()
		if city_name not in m_cities:
			m_cities[city_name] = city_id
	print len(m_cities)
	return m_cities


def get_zone_list_from_fliggy(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[2]:
			zone_list.append(field_list[4].strip())
	return zone_list


def get_zone_list_from_ctrip(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[0]:
			zone_list.append(field_list[2].strip())
	return zone_list


def get_zone_list_from_fliggy_city_pinyin(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == pypinyin.slug(unicode(field_list[2]), separator=''):
			zone_list.append(field_list[4])
	return zone_list


def percent2decimal(percent):
	return str(int(percent.replace('%', '')) / float(100))


def get_ratio(city_name, zone_name, file_name):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name in field_list[0] and zone_name in field_list[2]:
			if '0%' == field_list[3].strip():
				return '0.02'
			else:
				return percent2decimal(field_list[3].strip())


def calculate_similarity(zone_name, fliggy_zones):
	curr_similarity = -1
	curr_fliggy_zone = None
	for fliggy_zone in fliggy_zones:
		zone_name_py = pypinyin.slug(unicode(zone_name), separator='')
		fliggy_zone_py = pypinyin.slug(unicode(fliggy_zone), separator='')
		if Levenshtein.ratio(zone_name_py, fliggy_zone_py) > curr_similarity:
			curr_similarity = Levenshtein.ratio(zone_name_py, fliggy_zone_py)
			curr_fliggy_zone = fliggy_zone
	return curr_fliggy_zone


def get_zid_by_cname_zname(city_name, zone_name, file_name):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[2].strip() and zone_name == field_list[4].strip():
			return field_list[3].strip()


def process_single_zone(zone_name, fliggy_zones, city_name):
	match_list = []
	for fliggy_zone in fliggy_zones:
		ctrip_zone_name_pinyin = pypinyin.slug(unicode(zone_name), separator='')
		fliggy_zone_name_pinyin = pypinyin.slug(unicode(fliggy_zone), separator='')
		if ctrip_zone_name_pinyin in fliggy_zone_name_pinyin or fliggy_zone_name_pinyin in ctrip_zone_name_pinyin:
			match_list.append(fliggy_zone)
	if len(match_list) == 0:
		print '未匹配上'
	elif len(match_list) == 1:
		ratio = get_ratio(city_name, zone_name, ctrip_setp1_file_name)
		fliggy_zone_id = get_zid_by_cname_zname(city_name, match_list[0], fliggy_setp1_file_name)
		content = city_name + '\t' + fliggy_zone_id + '\t' + match_list[0] + '\t' + ratio + '\n'
		write2file(final_result_file_name, content)
	elif len(match_list) > 1:
		selected_zone = calculate_similarity(zone_name, match_list)
		ratio = get_ratio(city_name, zone_name, ctrip_setp1_file_name)
		fliggy_zone_id = get_zid_by_cname_zname(city_name, selected_zone, fliggy_setp1_file_name)
		content = city_name + '\t' + fliggy_zone_id + '\t' + selected_zone + '\t' + ratio + '\n'
		write2file(final_result_file_name, content)


def process_zone_group(zone_name, fliggy_zones, city_name):
	z_name_list = zone_name.split('/')
	total_match_list = []
	for z_name in z_name_list:
		match_list = []
		for fliggy_zone in fliggy_zones:
			ctrip_zone_name_pinyin = pypinyin.slug(unicode(z_name), separator='')
			fliggy_zone_name_pinyin = pypinyin.slug(unicode(fliggy_zone), separator='')
			if ctrip_zone_name_pinyin in fliggy_zone_name_pinyin or fliggy_zone_name_pinyin in ctrip_zone_name_pinyin:
				match_list.append(fliggy_zone)
		if len(match_list) == 0:
			break
		elif len(match_list) == 1:
			total_match_list.append(match_list[0])
		else:
			selected_zone = calculate_similarity(z_name, match_list)
			total_match_list.append(selected_zone)
	if len(z_name_list) == len(total_match_list):
		ratio = get_ratio(city_name, zone_name, ctrip_setp1_file_name)
		match_id_list = []
		for match in total_match_list:
			match_id_list.append(get_zid_by_cname_zname(city_name, match, fliggy_setp1_file_name))
		content = city_name + '\t' + '####'.join(match_id_list) + '\t' + '####'.join(
			total_match_list) + '\t' + ratio + '\n'
		write2file(final_result_file_name, content)


def match_zone(zone_name, fliggy_zones, city_name):
	# print str(fliggy_zones).decode('string_escape')
	if len(zone_name.split('/')) == 1:
		process_single_zone(zone_name, fliggy_zones, city_name)
	elif len(zone_name.split('/')) > 1:
		process_zone_group(zone_name, fliggy_zones, city_name)
	else:
		print 'ERROR ERROR ERROR ERROR'


def match_zones_list(ctrip_zones, fliggy_zones, city_name):
	# print str(ctrip_zones).decode('string_escape')
	# print str(fliggy_zones).decode('string_escape')
	for ctrip_zone in ctrip_zones:
		match_zone(ctrip_zone, fliggy_zones, city_name)


if __name__ == '__main__':
	ctrip_source_file_name = 'ctrip_hotel_guide_data_from_odps.txt'
	ctrip_setp1_file_name = 'ctrip_hotel_guide_data_step1.txt'
	fliggy_setp1_file_name = 'fliggy_zone_data_step1.txt'
	final_result_file_name = 'ctrip_final_result.txt'

	# JSON格式数据扁平化
	# for i in range(1, len(open(ctrip_source_file_name, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_source_file_name, i)
	# 	flat_json_data(line, ctrip_setp1_file_name)

	# 获取城市名称
	ctrip_cities_dict = get_ctrip_cities(ctrip_setp1_file_name)  # 197个城市, 其中155个城市在飞猪城市列表中
	fliggy_cities_dict = get_fliggy_cities(fliggy_setp1_file_name)  # 12326个城市
	# fliggy_cities_pinyin = [pypinyin.slug(unicode(city), separator='') for city in fliggy_cities_list]

	for ctrip_city in ctrip_cities_dict.keys():
		for (c_name, c_id) in fliggy_cities_dict.items():
			if ctrip_city == c_name:
				ctrip_zones_list = get_zone_list_from_ctrip(ctrip_city, ctrip_setp1_file_name)
				fliggy_zones_list = get_zone_list_from_fliggy(c_name, fliggy_setp1_file_name)
				match_zones_list(ctrip_zones_list, fliggy_zones_list, ctrip_city)
