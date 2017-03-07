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


if __name__ == '__main__':

	ctrip_cities_mapping_data_path = '../ctrip/ctrip_cities_mapping_data'
	haoqiao_cities_mapping_data_path = '../haoqiao/haoqiao_cities_mapping_data'

	ctrip_step1_file_path = '../ctrip/ctrip_step1_data_file'
	haoqiao_step1_file_path = '../haoqiao/haoqiao_step1_data_file'

	ctrip_step2_file_path = '../ctrip/ctrip_step2_data_file'
	haoqiao_step2_file_path = '../haoqiao/haoqiao_step2_data_file'

	fliggy_business_area_data = 'fliggy_business_area_data'

	all_distinct_city_ids = []
	for i in range(1, len(open(ctrip_cities_mapping_data_path, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_cities_mapping_data_path, i)
		split_fields = line.split('####')
		city_link = split_fields[0].strip()
		city_id = split_fields[1].strip()
		if int(city_id) >= 900000:
			all_distinct_city_ids.append(city_id)
	for i in range(1, len(open(haoqiao_cities_mapping_data_path, "rU").readlines()) + 1):
		line = linecache.getline(haoqiao_cities_mapping_data_path, i)
		split_fields = line.split('####')
		city_link = split_fields[0].strip()
		city_id = split_fields[1].strip()
		if int(city_id) >= 900000:
			all_distinct_city_ids.append(city_id)
	print len(set(all_distinct_city_ids))  # 200个城市

	all_distinct_cities = []
	all_distinct_areas = []
	for i in range(1, len(open(ctrip_step2_file_path, "rU").readlines()) + 1):
		line = linecache.getline(ctrip_step2_file_path, i)
		split_fields = line.split('\t')
		city_name = split_fields[1].strip()
		area_id = split_fields[3].strip()
		all_distinct_cities.append(city_name)
		all_distinct_areas.append(city_name + area_id)

	for i in range(1, len(open(haoqiao_step2_file_path, "rU").readlines()) + 1):
		line = linecache.getline(haoqiao_step2_file_path, i)
		split_fields = line.split('\t')
		city_name = split_fields[1].strip()
		area_id = split_fields[3].strip()
		all_distinct_cities.append(city_name)
		all_distinct_areas.append(city_name + area_id)
	print len(set(all_distinct_cities))  # 160个城市
	print len(set(all_distinct_areas))  # 606个商圈

	for city_id in set(all_distinct_city_ids):
		c_name = get_fliggy_city_name_by_city_id(fliggy_business_area_data, city_id)
		if c_name not in all_distinct_cities:
			print c_name



