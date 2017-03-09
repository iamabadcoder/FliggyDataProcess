# -*- coding:utf-8 -*-

from __future__ import division
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


def get_ctrip_city_name_by_city_link(file_name, city_link):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip():
			return split_fields[0]


def get_fliggy_city_name_by_city_id(file_name, city_id):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_id == split_fields[2].strip():
			return split_fields[3]


def get_all_ctrip_cities(file_name):
	ctrip_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_name = line.split('\t')[0].strip()
		city_link = line.split('\t')[1].strip()
		if city_name in ctrip_cities:
			if city_link != ctrip_cities[city_name]:
				print city_name
				print "ERROR ERROR ERROR"
		else:
			ctrip_cities[city_name] = city_link
	print len(ctrip_cities)
	return ctrip_cities


def get_all_fliggy_cities(file_name):
	fliggy_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		city_id = split_fields[2].strip()
		city_name = split_fields[3].strip()
		if city_id not in fliggy_cities:
			fliggy_cities[city_id] = city_name
	print len(fliggy_cities)
	return fliggy_cities


def get_ctrip_areas_by_city_link(file_name, city_link):
	ctrip_business_areas = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip():
			ctrip_business_areas.append(split_fields[2].strip())
	return ctrip_business_areas


def get_ctrip_hotels_by_city_link(file_name, city_link):
	ctrip_hotels = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip():
			ctrip_hotels.extend(split_fields[4].split('####'))
	return ctrip_hotels


def get_fliggy_areas_by_city_id(file_name, city_id):
	fliggy_areas = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_id == split_fields[2].strip():
			business_area_id = split_fields[0].strip()
			business_area_name = split_fields[1].strip()
			fliggy_areas[business_area_id] = business_area_name
	return fliggy_areas


def get_fliggy_hotels_by_city_id(file_name, city_id):
	fliggy_hotels = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_id == split_fields[2].strip():
			fliggy_hotels.extend(split_fields[4].split('####'))
	return fliggy_hotels


def calcu_selected_city_id(ctrip_city_link, matched_cities, ratio=None):
	max_intersec_count = 0
	selected_city_id = None
	for matched_city_id, matched_city_name in matched_cities.items():
		ctrip_hotels = get_ctrip_hotels_by_city_link(ctrip_step1_data_file, ctrip_city_link)
		fliggy_hotels = get_fliggy_hotels_by_city_id(fliggy_business_area_data, matched_city_id)
		intersec_count = len(set(ctrip_hotels).intersection(set(fliggy_hotels)))
		if ratio is None:
			if intersec_count >= max_intersec_count:
				selected_city_id = matched_city_id
		else:
			if round(intersec_count / len(ctrip_hotels), 2) > ratio:
				selected_city_id = matched_city_id
	return selected_city_id


def match_cities(ctrip_cities, fliggy_cities):
	for ctrip_city_name, ctrip_city_link in ctrip_cities.items():
		matched_cities = {}
		for fliggy_city_id, fliggy_city_name in fliggy_cities.items():
			if ctrip_city_name in fliggy_city_name:  # 城市名称相等
				matched_cities[fliggy_city_id] = fliggy_city_name
		if len(matched_cities) == 1:
			# content = ctrip_city_name + '####' + matched_cities[matched_cities.keys()[0]] + '\n'
			content = ctrip_city_link + '####' + matched_cities.keys()[0] + '\n'
			write2file(cities_mapping_data_file, content)
		elif len(matched_cities) > 1:
			selected_city_id = calcu_selected_city_id(ctrip_city_link, matched_cities, None)
			# content = ctrip_city_name + '####' + matched_cities[selected_city_id] + '\n'
			content = ctrip_city_link + '####' + selected_city_id + '\n'
			write2file(cities_mapping_data_file, content)
		elif len(matched_cities) < 1:
			for fliggy_city_id, fliggy_city_name in fliggy_cities.items():
				if ctrip_city_name in fliggy_city_name and ctrip_city_name != fliggy_city_name:
					matched_cities[fliggy_city_id] = fliggy_city_name
			if len(matched_cities) >= 1:
				selected_city_id = calcu_selected_city_id(ctrip_city_link, matched_cities, 0.2)
				if selected_city_id is not None:
					# content = ctrip_city_name + '####' + matched_cities[selected_city_id] + '\n'
					content = ctrip_city_link + '####' + selected_city_id + '\n'
					write2file(cities_mapping_data_file, content)


def get_ratio_by_city_link_and_area_name(file_name, city_link, area_name):
	ratio = None
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip() and area_name == split_fields[2].strip():
			ratio = split_fields[3].strip()
	return ratio


def get_ctrip_area_hotels_by_city_link_and_area_name(file_name, city_link, area_name):
	area_hotels = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip() and area_name == split_fields[2].strip():
			area_hotels.extend(split_fields[4].split('####'))
	return area_hotels


def get_fliggy_area_hotels_by_area_id(file_name, area_id):
	area_hotels = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if area_id == split_fields[0].strip():
			area_hotels.extend(split_fields[4].split('####'))
	return area_hotels



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
		business_area_link = business_area_info['businessAreaLink'].strip()
		business_area_name = business_area_info['businessAreaName'].strip()
		business_area_ratio = business_area_info['businessAreaRatio'].strip()
		if business_area_ratio == '0%':
			business_area_ratio = '5%'

		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k.strip() == business_area_name:
					content = city_name + '\t' + city_link + '\t' + business_area_name + '\t'
					content = content + business_area_ratio + '\t' + '####'.join(v) + '\n'
					write2file(output_file, content)


# 将JSON数据转换成二维表形式
def process_step1(input_file, output_file):
	for i in range(1, len(open(input_file, "rU").readlines()) + 1):
		line = linecache.getline(input_file, i)
		flat_ctrip_raw_data(line, output_file)


if __name__ == '__main__':
	ctrip_area_data_original = 'ctrip_area_data_original.txt'
	ctrip_area_data_step_1 = 'ctrip_area_data_step_1.txt'
	ctrip_area_data_step_2 = 'ctrip_area_data_step_2.txt'
	cities_mapping_data_file = 'ctrip_cities_mapping_data'
	fliggy_business_area_data = '../fliggy/fliggy_business_area_data'

	# JSON数据扁平化
	# process_step1(ctrip_area_data_original, ctrip_area_data_step_1)

	# 城市名称匹配
	# all_ctrip_cities = get_all_ctrip_cities(ctrip_area_data_step_1)  # 191
	# all_fliggy_cities = get_all_fliggy_cities(fliggy_business_area_data)  # 11626
	# match_cities(all_ctrip_cities, all_fliggy_cities)

	for i in range(1, len(open(cities_mapping_data_file, "rU").readlines()) + 1):
		print i
		line = linecache.getline(cities_mapping_data_file, i)
		split_fields = line.split('####')

		ctrip_city_link = split_fields[0].strip()
		ctrip_city_name = get_ctrip_city_name_by_city_link(ctrip_area_data_step_1, ctrip_city_link)
		fliggy_city_id = split_fields[1].strip()
		fliggy_city_name = get_fliggy_city_name_by_city_id(fliggy_business_area_data, fliggy_city_id)
		if int(fliggy_city_id) < 900000:
			continue
		all_ctrip_areas = get_ctrip_areas_by_city_link(ctrip_area_data_step_1, ctrip_city_link)
		all_fliggy_areas = get_fliggy_areas_by_city_id(fliggy_business_area_data, fliggy_city_id)

		for ctrip_area in all_ctrip_areas:
			for fliggy_area_id, fliggy_area_name in all_fliggy_areas.items():
				if ctrip_area == fliggy_area_name:  # 完全相等
					ratio = get_ratio_by_city_link_and_area_name(ctrip_area_data_step_1, ctrip_city_link, ctrip_area)
					content = ctrip_city_name + '\t' + fliggy_city_name + '\t' + ctrip_area + '\t'
					content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
					write2file(ctrip_area_data_step_2, content)
					break
				elif ctrip_area in fliggy_area_name or fliggy_area_name in ctrip_area:  # 包含关系(in)
					ctrip_area_hotels = get_ctrip_area_hotels_by_city_link_and_area_name(ctrip_area_data_step_1, ctrip_city_link, ctrip_area)
					fliggy_area_hotels = get_fliggy_area_hotels_by_area_id(fliggy_business_area_data, fliggy_area_id)
					intersec_count = len(set(ctrip_area_hotels).intersection(set(fliggy_area_hotels)))
					if len(ctrip_area_hotels) == 0:
						continue
					if round(intersec_count / len(ctrip_area_hotels), 4) > 0:
						ratio = get_ratio_by_city_link_and_area_name(ctrip_area_data_step_1, ctrip_city_link, ctrip_area)
						content = ctrip_city_name + '\t' + fliggy_city_name + '\t' + ctrip_area + '\t'
						content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
						write2file(ctrip_area_data_step_2, content)
						break
				else:
					ctrip_area_hotels = get_ctrip_area_hotels_by_city_link_and_area_name(ctrip_area_data_step_1, ctrip_city_link, ctrip_area)
					fliggy_area_hotels = get_fliggy_area_hotels_by_area_id(fliggy_business_area_data, fliggy_area_id)
					intersec_count = len(set(ctrip_area_hotels).intersection(set(fliggy_area_hotels)))
					if len(ctrip_area_hotels) == 0:
						continue
					if round(intersec_count / len(ctrip_area_hotels), 2) >= 0.1:
						ratio = get_ratio_by_city_link_and_area_name(ctrip_area_data_step_1, ctrip_city_link, ctrip_area)
						content = ctrip_city_name + '\t' + fliggy_city_name + '\t' + ctrip_area + '\t'
						content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
						write2file(ctrip_area_data_step_2, content)
						break
