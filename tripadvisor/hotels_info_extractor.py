# -*- coding:utf-8 -*-

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


def extract_one_city_hotel_info(city_line_num, input_file, output_file):
	city_name = linecache.getline(input_file, city_line_num).replace('#', '').strip()
	hotels_info_dict = {}
	hotels_info_dict['city_name'] = city_name

	hotels_info_list = []
	hotel_desc = ''
	hotel_dict = {}
	for i_line_num in range(city_line_num + 1, city_line_num + 100):
		i_line = linecache.getline(input_file, i_line_num)
		if i_line.count('#') == 2:
			break
		elif i_line.count('#') == 3:
			hotel_name = i_line.replace('#', '').strip()
			hotel_dict['hotel_name'] = hotel_name
		elif i_line.count('#') < 2 and '//www.tripadvisor.cn' not in i_line:
			hotel_desc += i_line.strip()
		elif '//www.tripadvisor.cn' in i_line:
			hotel_link = i_line.strip()
			hotel_dict['hotel_link'] = hotel_link
			hotel_link = ''
			hotel_dict['hotel_desc'] = hotel_desc
			hotel_desc = ''
			hotels_info_list.append(hotel_dict)
			hotel_dict = {}
	hotels_info_dict['hotels_info'] = hotels_info_list
	write2file(output_file, json.dumps(hotels_info_dict, ensure_ascii=False) + '\n')


def format_hotels_info_original(input_file, output_file):
	city_lines = []
	for i_line_num in range(1, len(open(input_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(input_file, i_line_num)
		if i_line.count('#') == 2:
			city_lines.append(i_line_num)

	for city_line_num in city_lines:
		extract_one_city_hotel_info(city_line_num, input_file, output_file)


if __name__ == '__main__':
	file_hotels_info = 'hotels_info.txt'
	file_hotels_info_original = 'hotels_info_original.txt'
	format_hotels_info_original(file_hotels_info_original, file_hotels_info)
