# -*- coding:utf-8 -*-

from __future__ import division
import re
import sys
import json
import uniout
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def clean(hotel_name, city_name):
	# replace stop words
	hotel_name = hotel_name.replace(city_name, '').replace('大酒店', '').replace('酒店', '').replace('客栈', '')
	hotel_name = hotel_name.replace('(', '').replace(')', '').strip()
	return hotel_name


def lcs_length(a, b):
	table = [[0] * (len(b) + 1) for _ in xrange(len(a) + 1)]
	for i, ca in enumerate(a, 1):
		for j, cb in enumerate(b, 1):
			table[i][j] = (table[i - 1][j - 1] + 1 if ca == cb else
						   max(table[i][j - 1], table[i - 1][j]))
	return table[-1][-1]


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def extract_ratio(desc):
	pattern = re.compile(r'(\d+%)')
	match = pattern.match(desc)
	if match:
		return match.group(1)
	else:
		return '2%'


def flat_haoqiao_data(data_line):
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
		area_id = area_info['businessAreaId']
		area_name = area_info['businessAreaTitle']
		if area_info.has_key('businessAreaDesc'):
			business_area_desc = area_info['businessAreaDesc']
		else:
			business_area_desc = '2%的游客选择住这里，-1家酒店'
		for hotel_info in json.loads(hotel_info_list):
			for (k, v) in hotel_info.items():
				if k.strip() == area_name.strip():
					ratio = extract_ratio(business_area_desc)
					content = city_name + '\t' + city_link + '\t' + area_name + '\t'
					content = content + ratio + '\t' + '####'.join(v) + '\n'
					write2file(haoqiao_area_data_step_1, content)
					break


def match_hotels(hq_hotels, f_hotels, city_name):
	matched_count = 0
	matched_result = None
	for hq_hotel in hq_hotels:
		for f_hotel in f_hotels:
			clean_hq_hotel = unicode(clean(hq_hotel, city_name))
			clean_f_hotel = unicode(clean(f_hotel, city_name))

			hq_hotel_len = len(clean_hq_hotel)
			f_hotel_len = len(clean_f_hotel)

			lcs_len = lcs_length(clean_hq_hotel, clean_f_hotel)
			min_len = min(hq_hotel_len, f_hotel_len)
			if min_len > 0 and lcs_len / min_len >= 0.7:
				matched_count += 1
				if matched_result is None:
					matched_result = f_hotel.strip()
				else:
					matched_result = matched_result + '@@@@' + f_hotel.strip()
				# break
	return matched_count, matched_result


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
	haoqiao_area_data_original = 'haoqiao_area_original.txt'
	haoqiao_area_data_step_1 = 'haoqiao_area_data_step_1.txt'
	haoqiao_area_data_step_2 = 'haoqiao_area_data_step_222.txt'
	fliggy_area_data_original = 'fliggy_area_data_original.txt'
	# for i in range(1, len(open(haoqiao_area_data_original, "rU").readlines()) + 1):
	# 	line = linecache.getline(haoqiao_area_data_original, i)
	# 	flat_haoqiao_data(line)

	init_fliggy_areas = init_fliggy_areas_by_city_name_key(fliggy_area_data_original)

	for i in range(241, 356):
		print i
		line = linecache.getline(haoqiao_area_data_step_1, i)
		hq_split_fields = line.split('\t')
		for i in range(len(hq_split_fields)):
			if i == 0:
				hq_city_name = hq_split_fields[i].strip()
			elif i == 1:
				hq_city_link = hq_split_fields[i].strip()
			elif i == 2:
				hq_area_name = hq_split_fields[i].strip()
			elif i == 3:
				hq_area_ratio = hq_split_fields[i].strip()
			elif i == 4:
				hq_hotel_list = hq_split_fields[i].strip().split('####')

		matched_hotels = {}
		matched_hotels_detail = {}
		if hq_city_name in init_fliggy_areas:
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
			matched_f_areas = None
			content = None
			if len(sorted_matched_hotels) >= 1:
				matched_f_areas = sorted_matched_hotels[0]
				content = hq_city_name + '\t' + hq_area_name + '\t' + hq_area_ratio + '\t' + '@@@@'.join(hq_hotel_list) + '\t'
				content = content + matched_f_areas + '\t' + matched_hotels_detail[sorted_matched_hotels[0]] + '\n'
			# elif len(sorted_matched_hotels) > 1:
			# 	matched_f_areas = sorted_matched_hotels[0] + '####' + sorted_matched_hotels[1]
			# 	content = hq_city_name + '\t' + hq_area_name + '\t' + hq_area_ratio + '\t' + matched_f_areas + '\t'
			# 	content = content + matched_hotels_detail[sorted_matched_hotels[0]] + '\t' + matched_hotels_detail[
			# 		sorted_matched_hotels[1]] + '\n'
			if content is not None:
				write2file(haoqiao_area_data_step_2, content)