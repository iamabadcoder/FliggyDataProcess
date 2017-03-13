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


def extract_target_lines(file_path, pattern):
	target_line_number_list = []
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith).strip()
		m = pattern.search(ith_line)
		if m is not None:
			target_line_number_list.append(ith)
	return target_line_number_list


if __name__ == '__main__':
	pound_sign = '#'
	dir_path = './baidu_md'
	all_citys = []
	file_count = 0
	highlight_pattern = re.compile(r'No\.\d+')  # 将正则表达式编译成 Pattern 对象
	for filtered_file in [afile for afile in os.listdir(dir_path) if 'html.md' in afile]:
		filtered_file_path = os.path.join(dir_path, filtered_file)
		dest_name = filtered_file.replace('.html.md', '').replace('百度旅游-', '').replace('攻略', '').strip()
		target_line_number_list = extract_target_lines(filtered_file_path, highlight_pattern)
		if len(target_line_number_list) == 0: continue
		highlight_sections = []
		for target_line in target_line_number_list:
			next_line = linecache.getline(filtered_file_path, target_line + 1).strip()
			next_next_line = linecache.getline(filtered_file_path, target_line + 2).strip()
			highlight_sec = {}
			if highlight_pattern.search(next_next_line) is None and next_next_line.count('#') >= next_line.count('#'):
				highlight_sections.append({clean_line(next_line): clean_line(next_next_line)})
			else:
				highlight_sections.append({'extra': clean_line(next_line)})
		if len(highlight_sections) > 0:
			mark_format = []
			for highlight_item in highlight_sections:
				for k, v in highlight_item.items():
					mark_format.append({'key': k, 'value': v})
			all_citys.append({"dest": dest_name, "亮点": mark_format})
	with open("baidu_highlight.json", 'w') as fout:
		fout.write(json.dumps(all_citys, ensure_ascii=False))
