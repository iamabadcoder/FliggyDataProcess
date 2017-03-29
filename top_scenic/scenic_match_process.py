# -*- coding:utf-8 -*-

import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def match_cities(file_name_1, file_name_2):
	# mafengwo
	mafengwo_city_list = []
	for i in range(1, len(open(file_name_1, "rU").readlines()) + 1):
		line = linecache.getline(file_name_1, i)
		mfw_city_name = line.split('\t')[1].strip()
		if mfw_city_name.endswith('市'):
			mafengwo_city_list.append(mfw_city_name.rstrip('市'))
		else:
			mafengwo_city_list.append(mfw_city_name)
	# fliggy
	fliggy_city_list = []
	for i in range(1, len(open(file_name_2, "rU").readlines()) + 1):
		line = linecache.getline(file_name_2, i)
		fliggy_city_name = line.split('\t')[2].strip()
		if fliggy_city_name.endswith('市'):
			fliggy_city_list.append(fliggy_city_name.rstrip('市'))
		else:
			fliggy_city_list.append(fliggy_city_name)

	print len(set(mafengwo_city_list))
	print len(set(fliggy_city_list))
	print str(len(set(mafengwo_city_list).intersection(set(fliggy_city_list))))


def init_fliggy_scenics(file_name):
	fliggy_scenic_dict = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i).strip()
		split_fields = line.split('\t')
		city_name = split_fields[2]
		if city_name.endswith('市'):
			city_name = city_name.rstrip('市')
		if city_name in fliggy_scenic_dict:
			fliggy_scenic_dict[city_name] = fliggy_scenic_dict[city_name] + '@@@@' + line
		else:
			fliggy_scenic_dict[city_name] = line
	return fliggy_scenic_dict


def filter_scenic(file_name):
	scenic_dict = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		line_split = line.split('\t')
		if line_split[4].strip() == 'NA' and line_split[5].strip() == 'NA':
			continue
		scenic_rank = line_split[2].strip()
		city_name = line_split[3].strip()
		scenic_id = line_split[4].strip()
		scenic_name = line_split[5].strip()

		key = city_name + scenic_id
		if key not in scenic_dict:
			scenic_dict[key] = line
			content = city_name + '\t' + scenic_id + '\t' + scenic_name + '\t' + scenic_rank + '\n'
			write2file(file_scenic_match_step2, content)


def match_scenic(mafengwo_file_name, fliggy_file_name):
	unmatched_count = 0
	matched_count = 0
	fliggy_scenic_dict = init_fliggy_scenics(fliggy_file_name)

	for i in range(1, len(open(mafengwo_file_name, "rU").readlines()) + 1):
		mafengwo_line = linecache.getline(mafengwo_file_name, i)
		mafengwo_city_name = mafengwo_line.split('\t')[1].strip()
		mafengwo_scenic_name = mafengwo_line.split('\t')[2].strip()
		if mafengwo_scenic_name.endswith('市'):
			mafengwo_scenic_name = mafengwo_scenic_name.rstrip('市')
		mafengwo_scenic_rank = mafengwo_line.split('\t')[3].strip()

		if mafengwo_city_name in fliggy_scenic_dict:
			matched_count += 1
			one_city_scenics = fliggy_scenic_dict[mafengwo_city_name]
			split_scenic_lines = one_city_scenics.split('@@@@')
			matched = False
			for scenic_line in split_scenic_lines:
				fliggy_scenic_id = scenic_line.split('\t')[0].strip()
				fliggy_scenic_name = scenic_line.split('\t')[1].strip()
				fliggy_city_name = scenic_line.split('\t')[2].strip()
				if fliggy_city_name.endswith('市'):
					fliggy_city_name = fliggy_city_name.rstrip('市')
				fliggy_province_name = scenic_line.split('\t')[3].strip()

				clean_mafengwo_scenic_name = mafengwo_scenic_name.replace(mafengwo_city_name, '')
				clean_fliggy_scenic_name = fliggy_scenic_name.replace(mafengwo_city_name, '')

				if mafengwo_scenic_name in fliggy_scenic_name or fliggy_scenic_name in mafengwo_scenic_name or clean_mafengwo_scenic_name == clean_fliggy_scenic_name:
					content = mafengwo_city_name + '\t' + mafengwo_scenic_name + '\t' + mafengwo_scenic_rank + '\t'
					content = content + fliggy_city_name + '\t' + fliggy_scenic_id + '\t' + fliggy_scenic_name + '\n'
					write2file(file_scenic_match_step1, content)
					matched = True
			if matched == False:
				content = mafengwo_city_name + '\t' + mafengwo_scenic_name + '\t' + mafengwo_scenic_rank + '\t'
				content = content + fliggy_city_name + '\t' + 'NA' + '\t' + 'NA' + '\n'
				write2file(file_scenic_match_step1, content)
				unmatched_count += 1
	print matched_count
	print unmatched_count

if __name__ == '__main__':
	file_fliggy_scenics = 'fliggy_scenics.txt'
	file_mafengwo_scenics = 'mafengwo_scenics.txt'
	file_scenic_match_step1 = 'scenic_match_step1.txt'
	file_scenic_match_step2 = 'scenic_match_step2.txt'

	# match_cities(file_mafengwo_scenics, file_fliggy_scenics)
	# filter_scenic(file_scenic_match_step1)
