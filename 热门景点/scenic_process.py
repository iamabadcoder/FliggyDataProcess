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
		line = linecache.getline(file_name, i)
		city_id = line.split('\t')[7].strip()
		city_name = line.split('\t')[8].strip()
		city_key = city_id + '####' + city_name
		if city_key in fliggy_scenic_dict:
			fliggy_scenic_dict[city_key] = fliggy_scenic_dict[city_key] + '@@@@' + line
		else:
			fliggy_scenic_dict[city_key] = line
	return fliggy_scenic_dict


if __name__ == '__main__':
	file_mafengwo_top_scenics = 'mafengwo_top_scenics.txt'
	file_fliggy_scenics_original = 'fliggy_scenics_original.txt'
	match_result = 'match_result.txt'
	# mafengwo_stat(file_mafengwo_top_scenics)
	# fliggy_stat(file_fliggy_scenics_original)
	# match_cities(file_mafengwo_top_scenics, file_fliggy_scenics_original)

	city_dict = {}
	for i in range(1, len(open(file_fliggy_scenics_original, "rU").readlines()) + 1):
		line = linecache.getline(file_fliggy_scenics_original, i)
		split_fields = line.split('\t')
		province_id = split_fields[7].strip()
		province_name = split_fields[8].strip()
		city_id = split_fields[7].strip()
		city_name = split_fields[8].strip()
		if city_name in city_dict:
			if province_name != city_dict[city_name]:
				print province_id, province_name, city_name, city_dict[city_name]
		else:
			city_dict[city_name] = province_name



		# for i in range(1, len(open(file_mafengwo_top_scenics, "rU").readlines()) + 1):
		# 	mafengwo_line = linecache.getline(file_mafengwo_top_scenics, i)
		# 	mafengwo_city_name = mafengwo_line.split('\t')[1].strip()
		# 	mafengwo_scenic_name = mafengwo_line.split('\t')[2].strip()
		# 	mafengwo_scenic_rank = mafengwo_line.split('\t')[3].strip()
		#
		# 	for i in range(1, len(open(file_fliggy_scenics_original, "rU").readlines()) + 1):
		# 		fliggy_line = linecache.getline(file_fliggy_scenics_original, i)
		# 		fliggy_titem_id = fliggy_line.split('\t')[0].strip()
		# 		fliggy_scenic_id = fliggy_line.split('\t')[1].strip()
		# 		fliggy_scenic_name = fliggy_line.split('\t')[2].strip()
		# 		fliggy_province_name = fliggy_line.split('\t')[6].strip()
		# 		fliggy_city_name = fliggy_line.split('\t')[8].strip()
		#
		# 		if mafengwo_city_name == fliggy_city_name or mafengwo_city_name == fliggy_province_name:
		# 			if mafengwo_scenic_name in fliggy_scenic_name or fliggy_scenic_name in mafengwo_scenic_name:
		# 				content = mafengwo_city_name + '\t' + mafengwo_scenic_name + '\t' + fliggy_province_name + '\t'
		# 				content = content + fliggy_city_name + '\t' + fliggy_scenic_id + '\t' + fliggy_scenic_name + '\t'
		# 				content = content + fliggy_titem_id + '\n'
		# 				write2file(match_result, content)
