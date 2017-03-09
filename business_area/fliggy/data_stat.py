# -*- coding:utf-8 -*-

import linecache


def get_fliggy_city_name_by_city_id(file_name, city_id):
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i)
		split_fields = line.split('\t')
		if city_id == split_fields[2].strip():
			return split_fields[3]

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

	oversea_area_result = 'oversea_area_result.txt'

	ctrip_area_data_step_2 = '../ctrip/ctrip_area_data_step_2.txt'
	ctrip_ratio_dict = {}
	ctrip_city_dict = {}
	for i in range(1, len(open(ctrip_area_data_step_2, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_area_data_step_2, i)
		split_fields = line.split('\t')
		f_area = split_fields[4].strip()
		f_area_id = split_fields[3].strip()
		key = f_area_id + '@@@@' + f_area
		if key not in ctrip_ratio_dict:
			ctrip_ratio_dict[key] = split_fields[5].strip()
		else:
			ctrip_ratio_dict[key] = ctrip_ratio_dict[key] + '####' + split_fields[5].strip()

		if key not in ctrip_city_dict:
			ctrip_city_dict[key] = split_fields[1].strip()
		else:
			ctrip_city_dict[key] = ctrip_city_dict[key] + '####' + split_fields[1].strip()

	haoqiao_step2_file_path = '../haoqiao/haoqiao_step2_data_file'
	haoqiao_ratio_dict = {}
	haoqiao_city_dict = {}
	for i in range(1, len(open(haoqiao_step2_file_path, "rU").readlines()) + 1):
		line = linecache.getline(haoqiao_step2_file_path, i)
		split_fields = line.split('\t')
		f_area = split_fields[4].strip()
		f_area_id = split_fields[3].strip()
		key = f_area_id + '@@@@' + f_area
		if key not in haoqiao_ratio_dict:
			haoqiao_ratio_dict[key] = split_fields[5].strip()
		else:
			haoqiao_ratio_dict[key] = haoqiao_ratio_dict[key] + '####' + split_fields[5].strip()

		if f_area not in haoqiao_city_dict:
			haoqiao_city_dict[key] = split_fields[1].strip()
		else:
			haoqiao_city_dict[key] = haoqiao_city_dict[key] + '####' + split_fields[1].strip()

	for k, v in ctrip_ratio_dict.iteritems():
		ratio_mean = 0.0
		if k in haoqiao_ratio_dict:
			split_ratios = v.split('####')
			split_ratios.extend(haoqiao_ratio_dict[k].split('####'))
			ratio_mean = avg_ratio(split_ratios)
		else:
			split_ratios = v.split('####')
			ratio_mean = avg_ratio(split_ratios)
		city_name = ctrip_city_dict[k].split('####')[0]
		content = k.split('@@@@')[0] + '\t' + k.split('@@@@')[1] + '\t' + str(ratio_mean) + '\t' + city_name + '\n'
		write2file(oversea_area_result, content)

	for k, v in haoqiao_ratio_dict.iteritems():
		ratio_mean = 0.0
		if k not in ctrip_ratio_dict:
			split_ratios = v.split('####')
			ratio_mean = avg_ratio(split_ratios)
			city_name = haoqiao_city_dict[k].split('####')[0]
			content = k.split('@@@@')[0] + '\t' + k.split('@@@@')[1] + '\t' + str(ratio_mean) + '\t' + city_name + '\n'
			write2file(oversea_area_result, content)









	# ctrip_cities_mapping_data_path = '../ctrip/ctrip_cities_mapping_data'
	# haoqiao_cities_mapping_data_path = '../haoqiao/haoqiao_cities_mapping_data'
	#
	# ctrip_step1_file_path = '../ctrip/ctrip_step1_data_file'
	# haoqiao_step1_file_path = '../haoqiao/haoqiao_step1_data_file'
	#
	# ctrip_step2_file_path = '../ctrip/ctrip_step2_data_file'
	# haoqiao_step2_file_path = '../haoqiao/haoqiao_step2_data_file'
	#
	# fliggy_business_area_data = 'fliggy_business_area_data'
	#
	# all_distinct_city_ids = []
	# for i in range(1, len(open(ctrip_cities_mapping_data_path, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_cities_mapping_data_path, i)
	# 	split_fields = line.split('####')
	# 	city_link = split_fields[0].strip()
	# 	city_id = split_fields[1].strip()
	# 	if int(city_id) >= 900000:
	# 		all_distinct_city_ids.append(city_id)
	# for i in range(1, len(open(haoqiao_cities_mapping_data_path, "rU").readlines()) + 1):
	# 	line = linecache.getline(haoqiao_cities_mapping_data_path, i)
	# 	split_fields = line.split('####')
	# 	city_link = split_fields[0].strip()
	# 	city_id = split_fields[1].strip()
	# 	if int(city_id) >= 900000:
	# 		all_distinct_city_ids.append(city_id)
	# print len(set(all_distinct_city_ids))  # 200个城市
	#
	# all_distinct_cities = []
	# all_distinct_areas = []
	# for i in range(1, len(open(ctrip_step2_file_path, "rU").readlines()) + 1):
	# 	line = linecache.getline(ctrip_step2_file_path, i)
	# 	split_fields = line.split('\t')
	# 	city_name = split_fields[1].strip()
	# 	area_id = split_fields[3].strip()
	# 	all_distinct_cities.append(city_name)
	# 	all_distinct_areas.append(city_name + area_id)
	#
	# for i in range(1, len(open(haoqiao_step2_file_path, "rU").readlines()) + 1):
	# 	line = linecache.getline(haoqiao_step2_file_path, i)
	# 	split_fields = line.split('\t')
	# 	city_name = split_fields[1].strip()
	# 	area_id = split_fields[3].strip()
	# 	all_distinct_cities.append(city_name)
	# 	all_distinct_areas.append(city_name + area_id)
	# print len(set(all_distinct_cities))  # 160个城市
	# print len(set(all_distinct_areas))  # 606个商圈
	#
	# for city_id in set(all_distinct_city_ids):
	# 	c_name = get_fliggy_city_name_by_city_id(fliggy_business_area_data, city_id)
	# 	if c_name not in all_distinct_cities:
	# 		print c_name



