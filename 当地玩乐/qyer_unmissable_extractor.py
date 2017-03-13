# -*- coding:utf-8 -*-

import os
import json
import linecache


# 写文件
def write_to_file(file_name, dest_name, content):
	file_object = open(file_name, 'a+')
	tour_record = {}
	tour_record['DESTINATION'] = dest_name
	tour_record['UNMISSABLE'] = content
	file_object.write("%s\n" % json.dumps(tour_record, ensure_ascii=False))
	file_object.flush()
	file_object.close()


def clean_line(line):
	return line.replace(prefix_sign, '').replace(postfix_sign, '').replace(pound_sign, '').strip()


def get_unmissable_title_line_nums(file_path, target_line_num):
	unmissable_title_line_nums = []
	for ith in range(target_line_num + 1, 500):
		ith_line = linecache.getline(file_path, ith)
		if ith_line is None:
			print 'error when get_unmissable_title_line_nums, %s, %s' % (file_path, ith)
			continue
		if ith_line.startswith('# '):
			break
		elif ith_line.startswith('## '):
			# print file_path, ith_line.strip()
			unmissable_title_line_nums.append(ith)
	return unmissable_title_line_nums


def locate_target_line(file_path):
	for ith in range(1, len(open(file_path, 'rU').readlines()) + 1):
		ith_line = linecache.getline(file_path, ith)
		if '# ___op___不可错过___ed___' == ith_line.strip():
			return ith
	return -1


def extract_one_unmissable_session(file_path, title_line_num):
	unmissable_session = {}
	unmissable_session_title = clean_line(linecache.getline(file_path, title_line_num))
	# print unmissable_session_title
	unmissable_session_desc = ''
	for ith in range(title_line_num + 1, title_line_num + 100):
		ith_line = linecache.getline(file_path, ith)
		if ith_line.startswith('## ') or ith_line.startswith('# '):
			break
		elif '图：' in ith_line:
			continue
		else:
			unmissable_session_desc += clean_line(ith_line)
	unmissable_session[unmissable_session_title] = unmissable_session_desc
	return unmissable_session


def extract_unmissable(file_path):
	unmissable_list = []
	target_line_num = locate_target_line(file_path)
	if target_line_num != -1:
		unmissable_title_line_nums = get_unmissable_title_line_nums(file_path, target_line_num)
		for ln in unmissable_title_line_nums:
			unmissable_session = extract_one_unmissable_session(file_path, ln)
			if len(unmissable_session) > 0: unmissable_list.append(unmissable_session)
	return unmissable_list


if __name__ == '__main__':
	prefix_sign = '___op___'
	postfix_sign = '___ed___'
	pound_sign = '#'
	dir_path = '/Users/caolei/Downloads/qyer/qyer_md/unmissable'
	all_citys = []
	for filtered_file in [afile for afile in os.listdir(dir_path) if 'html.md' in afile]:
		filtered_file_path = os.path.join(dir_path, filtered_file)
		if '纽约美食.html.md' not in filtered_file_path and '香港迪士尼乐园.html.md' not in filtered_file_path:
			print filtered_file_path
			unmissable_list = extract_unmissable(filtered_file_path)
			if len(unmissable_list) > 0:
				dest_name = filtered_file.replace('.html.md', '').replace('穷游锦囊 - ', '')
				mark_format = []
				for unmissable_item in unmissable_list:
					for k, v in unmissable_item.items():
						mark_format.append({'key': k, 'value': v})
				all_citys.append({"dest": dest_name, "不可错过": mark_format})
	with open("qyer_unmissable.json", 'w') as fout:
		fout.write(json.dumps(all_citys, ensure_ascii=False))
