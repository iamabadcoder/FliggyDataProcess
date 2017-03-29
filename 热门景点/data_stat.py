# -*- coding:utf-8 -*-

import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def stat_data():
	matched_city = {}
	unmatched_city = {}
	for i in range(1, len(open(match_result_step4, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step4, i)
		split_fields = line.split('\t')
		city_name = split_fields[0].strip()
		scenic_id = split_fields[1].strip()
		scenic_name = split_fields[2].strip()
		scenic_rank = split_fields[3].strip()
		item_title = split_fields[4].strip()

		if item_title == '未匹配上':
			if city_name in unmatched_city:
				tmp = unmatched_city[city_name]
				tmp.append(scenic_name)
				unmatched_city[city_name] = tmp
			else:
				unmatched_city[city_name] = [scenic_name]
			continue


		if city_name in matched_city:
			tmp = matched_city[city_name]
			tmp.append(scenic_name)
			matched_city[city_name] = tmp
		else:
			matched_city[city_name] = [scenic_name]


	for i in range(1, len(open(wan_le_step1, "rU").readlines()) + 1):
		line = linecache.getline(wan_le_step1, i)
		split_fields = line.split('\t')
		wan_le_city_name = split_fields[0].strip()
		wan_le_scenic_name = split_fields[2].strip()

		if wan_le_city_name in matched_city:
			tmp = matched_city[wan_le_city_name]
			tmp.append(wan_le_scenic_name)
			matched_city[wan_le_city_name] = tmp
		else:
			matched_city[wan_le_city_name] = [wan_le_scenic_name]

	# for k, v in matched_city.items():
	for k in matched_city:
		if k in unmatched_city:
			matched_set = set(matched_city[k])
			unmatch_set = set(unmatched_city[k])
			print k, len(matched_set | unmatch_set), len(matched_set)
		else:
			print k, len(matched_set), len(matched_set)



if __name__ == '__main__':

	city_dict = {}
	match_result_step4 = 'match_result_step4.txt'
	wan_le_step1 = 'wan_le_step1.txt'

	for i in range(1, len(open(match_result_step4, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step4, i)
		split_fields = line.split('\t')
		city_name = split_fields[0].strip()
		scenic_name = split_fields[2].strip()
		city_name = split_fields[0].strip()







