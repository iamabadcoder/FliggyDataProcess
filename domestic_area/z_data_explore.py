# -*- coding:utf-8 -*-
from __future__ import division
import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def avg_ratio(ratio_list):
	sum = 0.0
	if ratio_list is None:
		print 'ratio_list is None'
		return sum
	for ratio in ratio_list:
		sum += float(ratio[0:len(ratio) - 1]) / 100
	return round(sum / len(ratio_list), 4)


if __name__ == '__main__':
	# domestic_area_result = 'domestic_area_result.txt'
	oversea_area_result = '../business_area/fliggy/oversea_area_result.txt'

	area_list = []
	city_list = []
	for i in range(1, len(open(oversea_area_result, "rU").readlines()) + 1):
		line = linecache.getline(oversea_area_result, i)
		split_fields = line.split('\t')
		area_list.append(split_fields[0])
		city_list.append(split_fields[3])
	print len(area_list)
	print len(set(area_list))
	print len(set(city_list))





	# ctrip_area_step_3 = 'ctrip_area_step_3.txt'
	# ctrip_ratio_dict = {}
	# ctrip_city_dict = {}
	# for i in range(1, len(open(ctrip_area_step_3, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_area_step_3, i)
	# 	split_fields = line.split('\t')
	# 	f_area = split_fields[3].strip()
	# 	if f_area not in ctrip_ratio_dict:
	# 		ctrip_ratio_dict[f_area] = split_fields[2].strip()
	# 	else:
	# 		ctrip_ratio_dict[f_area] = ctrip_ratio_dict[f_area] + '####' + split_fields[2].strip()
	#
	# 	if f_area not in ctrip_city_dict:
	# 		ctrip_city_dict[f_area] = split_fields[0].strip()
	# 	else:
	# 		ctrip_city_dict[f_area] = ctrip_city_dict[f_area] + '####' + split_fields[0].strip()
	#
	# haoqiao_area_data_step_2 = 'haoqiao_area_data_step_2.txt'
	# haoqiao_ratio_dict = {}
	# haoqiao_city_dict = {}
	# for i in range(1, len(open(haoqiao_area_data_step_2, "rU").readlines()) + 1):
	# 	line = linecache.getline(haoqiao_area_data_step_2, i)
	# 	split_fields = line.split('\t')
	# 	f_area = split_fields[4].strip()
	# 	if f_area not in haoqiao_ratio_dict:
	# 		haoqiao_ratio_dict[f_area] = split_fields[2].strip()
	# 	else:
	# 		haoqiao_ratio_dict[f_area] = haoqiao_ratio_dict[f_area] + '####' + split_fields[2].strip()
	#
	# 	if f_area not in haoqiao_city_dict:
	# 		haoqiao_city_dict[f_area] = split_fields[0].strip()
	# 	else:
	# 		haoqiao_city_dict[f_area] = haoqiao_city_dict[f_area] + '####' + split_fields[0].strip()
	#
	# for k, v in ctrip_ratio_dict.iteritems():
	# 	ratio_mean = 0.0
	# 	if k in haoqiao_ratio_dict:
	# 		split_ratios = v.split('####')
	# 		split_ratios.extend(haoqiao_ratio_dict[k].split('####'))
	# 		ratio_mean = avg_ratio(split_ratios)
	# 	else:
	# 		split_ratios = v.split('####')
	# 		ratio_mean = avg_ratio(split_ratios)
	# 	city_name = ctrip_city_dict[k].split('####')[0]
	# 	content = k.split('@@@@')[0] + '\t' + k.split('@@@@')[1] + '\t' + str(ratio_mean) + '\t' + city_name + '\n'
	# 	write2file(domestic_area_result, content)
	#
	# for k, v in haoqiao_ratio_dict.iteritems():
	# 	ratio_mean = 0.0
	# 	if k not in ctrip_ratio_dict:
	# 		split_ratios = v.split('####')
	# 		ratio_mean = avg_ratio(split_ratios)
	# 		city_name = haoqiao_city_dict[k].split('####')[0]
	# 		content = k.split('@@@@')[0] + '\t' + k.split('@@@@')[1] + '\t' + str(ratio_mean) + '\t' + city_name + '\n'
	# 		write2file(domestic_area_result, content)



		# # print len(set(ctrip_cities))  # 58
		# # print len(set(ctrip_area_dict.keys()))  # 250
		#
		# haoqiao_area_data_step_2 = 'haoqiao_area_data_step_2.txt'
		# haoqiao_ratio_dict = {}
		# haoqiao_area_dict = {}
		# haoqiao_cities = []
		# for i in range(1, len(open(haoqiao_area_data_step_2, "rU").readlines()) + 1):
		# 	line = linecache.getline(haoqiao_area_data_step_2, i)
		# 	split_fields = line.split('\t')
		# 	haoqiao_cities.append(split_fields[0].strip())
		# 	haoqiao_ratio_dict[split_fields[0].strip() + '@@@@' + split_fields[1].strip()] = split_fields[2].strip()
		# 	haoqiao_area_dict[split_fields[0].strip() + '@@@@' + split_fields[1].strip()] = split_fields[4].strip()
		#
		# # print len(set(haoqiao_cities)) # 49
		# # print len(set(haoqiao_area_dict.keys())) # 294
		# # print len(set(haoqiao_cities).intersection(set(ctrip_cities))) # 40
		# print len(set(haoqiao_area_dict.keys()).intersection(set(ctrip_area_dict.keys()))) #
		#
		#
		# # for k, v in haoqiao_area_dict.iteritems():
		# # 	if k in haoqiao_area_dict:




		# haoqiao_area_data_original = 'haoqiao_area_original.txt'
		# ctrip_area_data_original = 'ctrip_area_original.txt'
		#
		# haoqiao_cities = []
		# for i in range(1, len(open(haoqiao_area_data_original, "rU").readlines()) + 1):
		# 	line = linecache.getline(haoqiao_area_data_original, i)
		# 	haoqiao_cities.append(line.split(',,,,,')[0])
		#
		# ctrip_cities = []
		# for i in range(1, len(open(ctrip_area_data_original, "rU").readlines()) + 1):
		# 	line = linecache.getline(ctrip_area_data_original, i)
		# 	ctrip_cities.append(line.split(',,,,,')[0])
		#
		# print len(haoqiao_cities)  # 67
		# print len(ctrip_cities)  # 62
		# print len(set(haoqiao_cities).intersection(set(ctrip_cities)))  # 49
		# print len(set(haoqiao_cities).union(set(ctrip_cities)))  # 80

		# ctrip_area_step_3 = 'ctrip_area_step_3.txt'
		# cities = []
		# for i in range(1, len(open(ctrip_area_step_3, "rU").readlines()) + 1):
		# 	line = linecache.getline(ctrip_area_step_3, i)
		# 	cities.append(line.split('\t')[0])
		# print len(set(cities))

		# haoqiao_area_data_step_1 = 'haoqiao_area_data_step_1.txt'
		# haoqiao_cities = []
		# for i in range(1, len(open(haoqiao_area_data_step_1, "rU").readlines()) + 1):
		# 	line = linecache.getline(haoqiao_area_data_step_1, i)
		# 	haoqiao_cities.append(line.split('\t')[0])
		# print len(set(haoqiao_cities))  # 67
		#
		# fliggy_area_data_original = 'fliggy_area_data_original.txt'
		# fliggy_cities = []
		# for i in range(1, len(open(fliggy_area_data_original, "rU").readlines()) + 1):
		# 	line = linecache.getline(fliggy_area_data_original, i)
		# 	fliggy_cities.append(line.split('\t')[3])
		# print len(set(fliggy_cities))  # 217
		#
		# print len(set(haoqiao_cities).intersection(set(fliggy_cities)))  # 49
