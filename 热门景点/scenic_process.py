# -*- coding:utf-8 -*-

import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def mafengwo_stat(file_name):
	city_name_list = []
	scenic_name_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		city_name_list.append(split_fields[1].strip())
		scenic_name_list.append(split_fields[0].strip() + '####' + split_fields[2].strip())
	print 'citys:' + str(len(set(city_name_list))) + ',scenics:' + str(len(set(scenic_name_list)))


def fliggy_stat(file_name):
	scenic_id_name_list = []
	city_name_list = []
	province_name_list = []
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		scenic_id_name_list.append(split_fields[1].strip() + '####' + split_fields[2].strip())
		city_name_list.append(split_fields[8].strip())
		province_name_list.append(split_fields[6].strip())
	print 'scenics:' + str(len(set(scenic_id_name_list))) + ',city:' + str(len(set(city_name_list)))
	print 'provinces:' + str(len(set(province_name_list)))


def match_cities(file_name_1, file_name_2):
	# mafengwo
	mafengwo_city_list = []
	for i in range(1, len(open(file_name_1, "rU").readlines()) + 1):
		line = linecache.getline(file_name_1, i)
		mafengwo_city_list.append(line.split('\t')[1].strip())

	# fliggy
	fliggy_city_list = []
	for i in range(1, len(open(file_name_2, "rU").readlines()) + 1):
		line = linecache.getline(file_name_2, i)
		fliggy_city_list.append(line.split('\t')[8].strip())

	print str(len(set(mafengwo_city_list).intersection(set(fliggy_city_list))))


def init_fliggy_scenic_data(file_name):
	fliggy_scenic_dict = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i).strip()
		city_name = line.split('\t')[8].strip()
		if city_name in fliggy_scenic_dict:
			fliggy_scenic_dict[city_name] = fliggy_scenic_dict[city_name] + '@@@@' + line
		else:
			fliggy_scenic_dict[city_name] = line
	return fliggy_scenic_dict


if __name__ == '__main__':
	file_mafengwo_top_scenics = 'mafengwo_top_scenics.txt'
	file_fliggy_scenics_original = 'fliggy_scenics_original.txt'
	match_result = 'match_result.txt'

	# mafengwo_stat(file_mafengwo_top_scenics)
	# fliggy_stat(file_fliggy_scenics_original)
	# match_cities(file_mafengwo_top_scenics, file_fliggy_scenics_original)

	fliggy_scenic_dict = init_fliggy_scenic_data(file_fliggy_scenics_original)

	titem_ids = []

	for i in range(1, len(open(file_mafengwo_top_scenics, "rU").readlines()) + 1):
		print i
		mafengwo_line = linecache.getline(file_mafengwo_top_scenics, i)
		mafengwo_city_name = mafengwo_line.split('\t')[1].strip()
		mafengwo_scenic_name = mafengwo_line.split('\t')[2].strip()
		mafengwo_scenic_rank = mafengwo_line.split('\t')[3].strip()

		if mafengwo_city_name in fliggy_scenic_dict:
			one_city_fliggy_scenics = fliggy_scenic_dict[mafengwo_city_name]
			fliggy_scenic_split_lines = one_city_fliggy_scenics.split('@@@@')
			for fliggy_scenic_line in fliggy_scenic_split_lines:
				fliggy_titem_id = fliggy_scenic_line.split('\t')[0].strip()
				fliggy_scenic_id = fliggy_scenic_line.split('\t')[1].strip()
				fliggy_scenic_name = fliggy_scenic_line.split('\t')[2].strip()
				fliggy_province_id = fliggy_scenic_line.split('\t')[5].strip()
				fliggy_province_name = fliggy_scenic_line.split('\t')[6].strip()
				fliggy_city_id = fliggy_scenic_line.split('\t')[7].strip()
				fliggy_city_name = fliggy_scenic_line.split('\t')[8].strip()
				if mafengwo_scenic_name in fliggy_scenic_name or fliggy_scenic_name in mafengwo_scenic_name:
					titem_ids.append(fliggy_titem_id)
					content = fliggy_province_id + '\t' + fliggy_province_name + '\t' + fliggy_city_id + '\t'
					content = content + fliggy_city_name + '\t' + fliggy_scenic_id + '\t' + fliggy_scenic_name + '\t'
					content = content + mafengwo_scenic_rank + '\t' + fliggy_titem_id + '\n'
					write2file(match_result, content)
	print len(set(titem_ids))
