# -*- coding:utf-8 -*-

import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def flat_similarity_data(input_file, output_file):
	for i in range(1, len(open(input_file, "rU").readlines()) + 1):
		line = linecache.getline(input_file, i)
		line_split_fields = line.split('\t')
		city_name = line_split_fields[0].strip()
		similarity_data = line_split_fields[1].strip()
		if similarity_data.startswith('-'):
			continue
		for similarity_section in similarity_data.split(';'):
			similarity_city_name = similarity_section.split(',')[0].strip()
			similarity_value = similarity_section.split(',')[1].strip()
			content = city_name + '\t' + similarity_city_name + '\t' + similarity_value + '\n'
			write2file(output_file, content)


# {province_id:province_name}
def init_province_dict(input_file_name):
	province_dict = {}
	for i in range(1, len(open(input_file_name, "rU").readlines()) + 1):
		line = linecache.getline(input_file_name, i)
		line_split_fields = line.split('\t')
		pro_name = line_split_fields[0].strip()
		pro_id = line_split_fields[1].strip()
		province_dict[pro_id] = pro_name
	return province_dict


# {city_name:city_id}
def init_city_dict(input_file_name):
	city_dict = {}
	for i in range(1, len(open(input_file_name, "rU").readlines()) + 1):
		line = linecache.getline(input_file_name, i)
		line_split_fields = line.split('\t')
		city_name = line_split_fields[0].strip()
		city_id = line_split_fields[1].strip()
		# 国内/国外过滤控制
		if int(city_id) < 900000:
			city_dict[city_name] = city_id
	return city_dict


# {city_id:province_id}
def init_city_province_mapping_dict(input_file_name):
	city_province_mapping_dict = {}
	for i in range(1, len(open(input_file_name, "rU").readlines()) + 1):
		line = linecache.getline(input_file_name, i)
		line_split_fields = line.split('\t')
		province_id = line_split_fields[0].strip()
		city_id = line_split_fields[1].strip()
		city_province_mapping_dict[city_id] = province_id
	return city_province_mapping_dict


if __name__ == '__main__':
	file_province2code = 'province2code.txt'
	file_city2code = 'city2code.txt'
	file_province_city_mapping = 'province_city_mapping.txt'
	file_similarity_step1 = 'similarity_step1.txt'
	file_similarity_step2 = 'similarity_step2.txt'
	file_similarity_step3 = 'similarity_step3.txt'

	# flat_similarity_data(file_similarity_step1, file_similarity_step2)
	city_count_list = []

	province_dict = init_province_dict(file_province2code)
	print len(province_dict)
	city_dict = init_city_dict(file_city2code)
	print len(city_dict)
	city_province_mapping_dict = init_city_province_mapping_dict(file_province_city_mapping)
	print len(city_province_mapping_dict)

	for i in range(1, len(open(file_similarity_step2, "rU").readlines()) + 1):
		line = linecache.getline(file_similarity_step2, i)
		line_split_fields = line.split('\t')
		city_a = line_split_fields[0].strip()
		city_b = line_split_fields[1].strip()
		similarity_value = line_split_fields[2].strip()

		# 相同城市过滤掉
		if city_a == city_b:
			continue

		# 过滤出国内城市
		if city_a not in city_dict or city_b not in city_dict:
			continue

		# 过滤掉省份(一个城市和一个省份对比意义不大)
		if city_a not in ['北京', '上海', '天津', '重庆'] and city_b not in ['北京', '上海', '天津', '重庆']:
			if city_a in province_dict.values() or city_b in province_dict.values():
				continue

		city_a_id = city_dict[city_a]
		city_b_id = city_dict[city_b]

		pro_a_id = city_province_mapping_dict[city_a_id]
		pro_b_id = city_province_mapping_dict[city_b_id]

		if pro_a_id is None or pro_b_id is None:
			print city_dict[city_a], city_dict[city_b]
			continue

		pro_a_name = province_dict[pro_a_id]
		pro_b_name = province_dict[pro_b_id]
		if pro_a_name is None or pro_b_name is None:
			print pro_a_id, pro_b_id
			continue
		city_count_list.append(city_a)
		content = city_a_id + '\t' + city_a + '\t' + pro_a_id + '\t' + pro_a_name + '\t'
		content = content + city_b_id + '\t' + city_b + '\t' + pro_b_id + '\t' + pro_b_name + '\t'
		content = content + similarity_value + '\n'

		write2file(file_similarity_step3, content)
	print len(set(city_count_list))
