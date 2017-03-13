# -*- coding:utf-8 -*-

import os
import re
import json
import linecache


def locate_target_line(file_path, dest_name):
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith)
		target_line = '# ' + dest_name + '必玩'
		if target_line == ith_line.strip() or '# 目的地必玩' == ith_line.strip():
			return ith
	return -1


def clean_line(line):
	return line.replace(pound_sign, '').strip()


def extract_target_line(file_path):
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith).strip()
		if ith_line.endswith('I WANNA'):
			return ith
	return -1


if __name__ == '__main__':
	pound_sign = '#'
	dir_path = '/Users/caolei/Downloads/baidu/baidu_md/backup'
	all_citys = []
	file_count = 0
	unmissable_pattern = re.compile(r'\d+')  # 将正则表达式编译成 Pattern 对象
	for filtered_file in [afile for afile in os.listdir(dir_path) if 'html.md' in afile]:
		filtered_file_path = os.path.join(dir_path, filtered_file)
		dest_name = filtered_file.replace('.html.md', '').replace('百度旅游-', '').replace('攻略', '').strip()
		target_line_num = extract_target_line(filtered_file_path)
		if target_line_num == -1: continue
		next_next_line = linecache.getline(filtered_file_path, target_line_num + 2).replace('#', '').strip()
		i_wanna_list = unmissable_pattern.split(next_next_line)
		wanna_sections = []
		for i in range(1, len(i_wanna_list)):
			wanna_sections.append({i: i_wanna_list[i]})
		if len(wanna_sections) > 0:
			mark_format = []
			for wanna_item in wanna_sections:
				for k, v in wanna_item.items():
					mark_format.append({'key': k, 'value': v})
			all_citys.append({"dest": dest_name, "不可错过": mark_format})
	with open("baidu_unmissable.json", 'w') as fout:
		fout.write(json.dumps(all_citys, ensure_ascii=False))
