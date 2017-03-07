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


def get_haoqiao_city_name_by_city_link(file_name, city_link):
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


def get_all_haoqiao_cities(file_name):
	haoqiao_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		city_name = line.split('\t')[0].strip()
		city_link = line.split('\t')[1].strip()
		if city_name in haoqiao_cities.keys():
			if city_link != haoqiao_cities[city_name]:
				print "ERROR ERROR ERROR", city_name
		else:
			haoqiao_cities[city_name] = city_link
	print len(haoqiao_cities)
	return haoqiao_cities


def get_all_fliggy_cities(file_name):
	fliggy_cities = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		city_id = split_fields[2].strip()
		city_name = split_fields[3].strip()
		if city_id not in fliggy_cities.keys():
			fliggy_cities[city_id] = city_name
	print len(fliggy_cities)
	return fliggy_cities


def get_haoqiao_areas_by_city_link(file_name, city_link):
	haoqiao_business_areas = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip():
			haoqiao_business_areas.append(split_fields[2].strip())
	return haoqiao_business_areas


def get_haoqiao_hotels_by_city_link(file_name, city_link):
	haoqiao_hotels = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip():
			haoqiao_hotels.extend(split_fields[4].split('####'))
	return haoqiao_hotels


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


def calcu_selected_city_id(haoqiao_city_link, matched_cities, ratio=None):
	max_intersec_count = 0
	selected_city_id = None
	for matched_city_id, matched_city_name in matched_cities.items():
		haoqiao_hotels = get_haoqiao_hotels_by_city_link(haoqiao_step1_data_file, haoqiao_city_link)
		fliggy_hotels = get_fliggy_hotels_by_city_id(fliggy_business_area_data, matched_city_id)
		intersec_count = len(set(haoqiao_hotels).intersection(set(fliggy_hotels)))
		if ratio is None:
			if intersec_count >= max_intersec_count:
				selected_city_id = matched_city_id
		else:
			if round(intersec_count / len(haoqiao_hotels), 2) > ratio:
				selected_city_id = matched_city_id
	return selected_city_id


def match_cities(haoqiao_cities, fliggy_cities):
	for haoqiao_city_name, haoqiao_city_link in haoqiao_cities.items():
		matched_cities = {}
		for fliggy_city_id, fliggy_city_name in fliggy_cities.items():
			if haoqiao_city_name in fliggy_city_name:
				matched_cities[fliggy_city_id] = fliggy_city_name
		if len(matched_cities) == 1:
			# content = haoqiao_city_name + '####' + matched_cities[matched_cities.keys()[0]] + '\n'
			content = haoqiao_city_link + '####' + matched_cities.keys()[0] + '\n'
			write2file(cities_mapping_data_file, content)
		elif len(matched_cities) > 1:
			selected_city_id = calcu_selected_city_id(haoqiao_city_link, matched_cities, None)
			# content = haoqiao_city_name + '####' + matched_cities[selected_city_id] + '\n'
			content = haoqiao_city_link + '####' + selected_city_id + '\n'
			write2file(cities_mapping_data_file, content)
		elif len(matched_cities) < 1:
			for fliggy_city_id, fliggy_city_name in fliggy_cities.items():
				if haoqiao_city_name in fliggy_city_name and haoqiao_city_name != fliggy_city_name:
					matched_cities[fliggy_city_id] = fliggy_city_name
			if len(matched_cities) >= 1:
				selected_city_id = calcu_selected_city_id(haoqiao_city_link, matched_cities, 0.2)
				if selected_city_id is not None:
					# content = haoqiao_city_name + '####' + matched_cities[selected_city_id] + '\n'
					content = haoqiao_city_link + '####' + selected_city_id + '\n'
					write2file(cities_mapping_data_file, content)


def get_ratio_by_city_link_and_area_name(file_name, city_link, area_name):
	ratio = None
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_link == split_fields[1].strip() and area_name == split_fields[2].strip():
			ratio = split_fields[3].strip()
	return ratio


def get_haoqiao_area_hotels_by_city_link_and_area_name(file_name, city_link, area_name):
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


if __name__ == '__main__':
	haoqiao_step1_data_file = './haoqiao_step1_data_file'
	haoqiao_step2_data_file = './haoqiao_step2_data_file'
	cities_mapping_data_file = './haoqiao_cities_mapping_data'
	fliggy_business_area_data = '../fliggy/fliggy_business_area_data'

	# 城市名称匹配
	# all_haoqiao_cities = get_all_haoqiao_cities(haoqiao_step1_data_file)
	# all_fliggy_cities = get_all_fliggy_cities(fliggy_business_area_data)
	# match_cities(all_haoqiao_cities, all_fliggy_cities)

	for i in range(1, len(open(cities_mapping_data_file, "rU").readlines()) + 1):
		line = linecache.getline(cities_mapping_data_file, i)
		split_fields = line.split('####')

		haoqiao_city_link = split_fields[0].strip()
		haoqiao_city_name = get_haoqiao_city_name_by_city_link(haoqiao_step1_data_file, haoqiao_city_link)
		fliggy_city_id = split_fields[1].strip()
		fliggy_city_name = get_fliggy_city_name_by_city_id(fliggy_business_area_data, fliggy_city_id)
		if int(fliggy_city_id) < 900000:
			continue

		all_haoqiao_areas = get_haoqiao_areas_by_city_link(haoqiao_step1_data_file, haoqiao_city_link)
		all_fliggy_areas = get_fliggy_areas_by_city_id(fliggy_business_area_data, fliggy_city_id)

		for haoqiao_area in all_haoqiao_areas:
			for fliggy_area_id, fliggy_area_name in all_fliggy_areas.items():
				if haoqiao_area == fliggy_area_name:  # 完全相等
					ratio = get_ratio_by_city_link_and_area_name(haoqiao_step1_data_file, haoqiao_city_link, haoqiao_area)
					content = haoqiao_city_name + '\t' + fliggy_city_name + '\t' + haoqiao_area + '\t'
					content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
					write2file(haoqiao_step2_data_file, content)
					break
				elif haoqiao_area in fliggy_area_name or fliggy_area_name in haoqiao_area:  # 包含关系(in)
					haoqiao_area_hotels = get_haoqiao_area_hotels_by_city_link_and_area_name(haoqiao_step1_data_file, haoqiao_city_link, haoqiao_area)
					fliggy_area_hotels = get_fliggy_area_hotels_by_area_id(fliggy_business_area_data, fliggy_area_id)
					intersec_count = len(set(haoqiao_area_hotels).intersection(set(fliggy_area_hotels)))
					if len(haoqiao_area_hotels) == 0:
						continue
					if round(intersec_count / len(haoqiao_area_hotels), 4) > 0:
						ratio = get_ratio_by_city_link_and_area_name(haoqiao_step1_data_file, haoqiao_city_link, haoqiao_area)
						content = haoqiao_city_name + '\t' + fliggy_city_name + '\t' + haoqiao_area + '\t'
						content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
						write2file(haoqiao_step2_data_file, content)
						break
				else:
					haoqiao_area_hotels = get_haoqiao_area_hotels_by_city_link_and_area_name(haoqiao_step1_data_file, haoqiao_city_link, haoqiao_area)
					fliggy_area_hotels = get_fliggy_area_hotels_by_area_id(fliggy_business_area_data, fliggy_area_id)
					intersec_count = len(set(haoqiao_area_hotels).intersection(set(fliggy_area_hotels)))
					if len(haoqiao_area_hotels) == 0:
						continue
					if round(intersec_count / len(haoqiao_area_hotels), 2) >= 0.1:
						ratio = get_ratio_by_city_link_and_area_name(haoqiao_step1_data_file, haoqiao_city_link, haoqiao_area)
						content = haoqiao_city_name + '\t' + fliggy_city_name + '\t' + haoqiao_area + '\t'
						content = content + fliggy_area_id + '\t' + fliggy_area_name + '\t' + ratio + '\n'
						write2file(haoqiao_step2_data_file, content)
						break
