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


def extract_accommodation_info(file_path, target_line_num, destination):
	accommodation_info = ''
	for i_line_num in range(target_line_num + 1, target_line_num + 50):
		i_line = linecache.getline(file_path, i_line_num)
		if '更多酒店信息' in i_line:
			break
		elif '●' in i_line:
			accommodation_info += i_line.replace('#', '').replace('●', '').lstrip()
		elif '◆' in i_line:
			accommodation_info += i_line.replace('#', '').replace('◆', '').lstrip()
		elif accommodation_info != '':
			accommodation_info = accommodation_info.rstrip('\n') + i_line.replace('#', '').lstrip()
		else:
			print destination, i_line_num
			print 'ERROR WHEN extract_accommodation_info'
	if accommodation_info != '':
		res_dict = {}
		res_dict['destination'] = destination
		res_dict['accommodation_info'] = accommodation_info.strip()
		write2file(file_accommodation_info, json.dumps(res_dict, ensure_ascii=False) + '\n')


def locate_target_line(input_file):
	destination = filtered_file.replace('.html.md', '')
	file_path = os.path.join(dir_path, input_file)
	for i_line_num in range(1, len(open(file_path, 'rU').readlines()) + 1):
		i_line = linecache.getline(file_path, i_line_num)
		if '如何选择适合您的住宿' in i_line:
			extract_accommodation_info(file_path, i_line_num, destination)
			break


if __name__ == '__main__':
	file_accommodation_info = 'accommodation_info.txt'
	dir_path = '/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/md'
	file_list = os.listdir(dir_path)
	for filtered_file in [afile for afile in file_list if 'html.md' in afile]:
		locate_target_line(filtered_file)
