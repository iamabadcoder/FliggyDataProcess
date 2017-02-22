# -*- coding:utf-8 -*-

import re
import sys
import json
import pypinyin
import linecache
import Levenshtein

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def falt_json_data(data_line):
	field_list = data_line.split(',')
	for i in range(len(field_list)):
		if i == 1:
			country_name = field_list[i].strip()
		elif i == 2:
			country_link = field_list[i].strip()
		elif i == 3:
			city_name = field_list[i].strip()
		elif i == 4:
			city_link = field_list[i].strip()
		elif i >= 5:
			zone_info = ','.join(field_list[5:len(field_list)])
			break
	for zone in json.loads(zone_info)['zoneInfo']:
		zone_desc = None
		for key in zone:
			if 'zoneNameCh' in key:
				zone_name_ch = zone['zoneNameCh'].strip()
			elif 'zoneDesc' in key:
				zone_desc = zone['zoneDesc'].strip()
			if zone_desc is not None:
				search_res = re.search(ur'(\d+%) 的游客选择住这里', unicode(zone_desc), re.S)
				if search_res:
					select_ratio = search_res.group(1).strip()
				else:
					select_ratio = '0%'
		write2file(haoqiao_setp1_file_name,
				   country_name + '\t' + country_link + '\t' + city_name + '\t' + city_link + '\t' + zone_name_ch + '\t' + select_ratio + '\n')


def get_haoqiao_cities(file_name):
	m_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_name = line.split('\t')[2].strip()
		city_link = line.split('\t')[3].strip()
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


def percent2decimal(percent):
	return str(int(percent.replace('%', '')) / float(100))


def get_ratio(city_name, zone_name, file_name):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[2] and zone_name == field_list[4]:
			if '0%' == field_list[5].strip():
				return '0.02'
			else:
				return percent2decimal(field_list[5].strip())


def get_zone_list_from_haoqiao(city_name, file_name):
	zone_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		field_list = line.split('\t')
		if city_name == field_list[2]:
			zone_list.append(field_list[4].strip())
	return zone_list


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
		haoqiao_zone_name_pinyin = pypinyin.slug(unicode(zone_name), separator='')
		fliggy_zone_name_pinyin = pypinyin.slug(unicode(fliggy_zone), separator='')
		if haoqiao_zone_name_pinyin in fliggy_zone_name_pinyin or fliggy_zone_name_pinyin in haoqiao_zone_name_pinyin:
			match_list.append(fliggy_zone)
	if len(match_list) == 0:
		print '未匹配上'
	elif len(match_list) == 1:
		ratio = get_ratio(city_name, zone_name, haoqiao_setp1_file_name)
		fliggy_zone_id = get_zid_by_cname_zname(city_name, match_list[0], fliggy_setp1_file_name)
		content = city_name + '\t' + fliggy_zone_id + '\t' + match_list[0] + '\t' + ratio + '\n'
		write2file(final_result_file_name, content)
	elif len(match_list) > 1:
		selected_zone = calculate_similarity(zone_name, match_list)
		ratio = get_ratio(city_name, zone_name, haoqiao_setp1_file_name)
		fliggy_zone_id = get_zid_by_cname_zname(city_name, selected_zone, fliggy_setp1_file_name)
		content = city_name + '\t' + fliggy_zone_id + '\t' + selected_zone + '\t' + ratio + '\n'
		write2file(final_result_file_name, content)


def process_zone_group(zone_name, fliggy_zones, city_name):
	z_name_list = zone_name.split('/')
	total_match_list = []
	for z_name in z_name_list:
		match_list = []
		for fliggy_zone in fliggy_zones:
			haoqiao_zone_name_pinyin = pypinyin.slug(unicode(z_name), separator='')
			fliggy_zone_name_pinyin = pypinyin.slug(unicode(fliggy_zone), separator='')
			if haoqiao_zone_name_pinyin in fliggy_zone_name_pinyin or fliggy_zone_name_pinyin in haoqiao_zone_name_pinyin:
				match_list.append(fliggy_zone)
		if len(match_list) == 0:
			break
		elif len(match_list) == 1:
			total_match_list.append(match_list[0])
		else:
			selected_zone = calculate_similarity(z_name, match_list)
			total_match_list.append(selected_zone)
	if len(z_name_list) == len(total_match_list):
		ratio = get_ratio(city_name, zone_name, haoqiao_setp1_file_name)
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


def match_zones_list(haoqiao_zones, fliggy_zones, city_name):
	for haoqiao_zone in haoqiao_zones:
		match_zone(haoqiao_zone, fliggy_zones, city_name)


if __name__ == '__main__':
	haoqiao_source_file_name = 'haoqiao_hotel_guide_data_from_odps.txt'
	haoqiao_setp1_file_name = 'haoqiao_hotel_guide_data_step1.txt'
	fliggy_setp1_file_name = 'fliggy_zone_data_step1.txt'
	final_result_file_name = 'haoqiao_final_result.txt'

	# 将JSON数据转换成二维表形式
	# for i in range(1, len(open(haoqiao_source_file_name, "rU").readlines()) + 1):
	# 	line = linecache.getline(haoqiao_source_file_name, i)
	# 	falt_json_data(line)

	# 获取城市名称
	haoqiao_cities_dict = get_haoqiao_cities(haoqiao_setp1_file_name)  # 142个城市, 其中117个城市能匹配上飞猪的城市
	fliggy_cities_dict = get_fliggy_cities(fliggy_setp1_file_name)  # 12326个城市

	for haoqiao_city in haoqiao_cities_dict.keys():
		for (c_name, c_id) in fliggy_cities_dict.items():
			if haoqiao_city == c_name:
				haoqiao_zones_list = get_zone_list_from_haoqiao(haoqiao_city, haoqiao_setp1_file_name)
				fliggy_zones_list = get_zone_list_from_fliggy(c_name, fliggy_setp1_file_name)
				match_zones_list(haoqiao_zones_list, fliggy_zones_list, haoqiao_city)
