# -*- coding:utf-8 -*-

import os
import json
import linecache


def clean_line(line):
	return line.replace(pound_sign, '').strip()


def get_play_title_title_line_nums(file_path, target_line_num):
	must_play_title_line_nums = []
	for ith in range(target_line_num + 1, 2000):
		ith_line = linecache.getline(file_path, ith)
		if ith_line is None:
			print 'error when get_play_title_title_line_nums, %s, %s' % (file_path, ith)
			continue
		if ith_line.startswith('# '):
			break
		elif ith_line.startswith('## '):
			# print file_path, ith_line.strip()
			must_play_title_line_nums.append(ith)
	return must_play_title_line_nums


def locate_target_line(file_path, dest_name):
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith)
		target_line = '# ' + dest_name + '必玩'
		if target_line == ith_line.strip() or '# 目的地必玩' == ith_line.strip():
			return ith
	return -1


def extract_one_must_play_session(file_path, title_line_num):
	must_play_session = {}
	must_play_session_title = clean_line(linecache.getline(file_path, title_line_num))
	# print unmissable_session_title
	must_play_session_desc = ''
	for ith in range(title_line_num + 1, title_line_num + 100):
		ith_line = linecache.getline(file_path, ith)
		if ith_line.startswith('## ') or ith_line.startswith('# '):
			break
		elif '该图片由' in ith_line:
			continue
		else:
			must_play_session_desc += clean_line(ith_line)
	must_play_session[must_play_session_title] = must_play_session_desc
	return must_play_session


def extract_must_play(file_path, dest_name):
	must_play_list = []
	target_line_num = locate_target_line(file_path, dest_name)
	if target_line_num != -1:
		must_play_title_line_nums = get_play_title_title_line_nums(file_path, target_line_num)
		for ln in must_play_title_line_nums:
			must_play_session = extract_one_must_play_session(file_path, ln)
			if len(must_play_session) > 0:
				must_play_list.append(must_play_session)
	return must_play_list


if __name__ == '__main__':
	pound_sign = '#'
	dir_path = './ctrip_md'
	all_citys = []
	file_count = 0
	for filtered_file in [afile for afile in os.listdir(dir_path) if 'html.md' in afile]:
		filtered_file_path = os.path.join(dir_path, filtered_file)
		dest_name = filtered_file.replace('.html.md', '').replace('旅游攻略', '').strip()
		must_play_list = extract_must_play(filtered_file_path, dest_name)
		if len(must_play_list) > 0:
			mark_format = []
			for must_play_item in must_play_list:
				for k, v in must_play_item.items():
					mark_format.append({'key': k, 'value': v})
			all_citys.append({"dest": dest_name, "目的地必玩": mark_format})
with open("ctrip_must_play.json", 'w') as fout:
	fout.write(json.dumps(all_citys, ensure_ascii=False))
