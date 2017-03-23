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


def clean_step1_data():
	titem_ids = []
	titem_dict = {}
	for i in range(1, len(open(match_result_step1, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step1, i)
		split_fields = line.split('\t')
		titem_id = split_fields[7].strip()
		scenic_rank = split_fields[2].strip()

		if titem_id == 'NA':
			write2file(match_result_step2, line)
			continue

		if titem_id not in titem_ids:
			titem_ids.append(titem_id)
			titem_dict[titem_id] = line
		else:
			pre_line = titem_dict[titem_id]
			pre_scenic_rank = pre_line.split()[2].strip()
			if int(pre_scenic_rank) > int(scenic_rank):
				titem_dict[titem_id] = line
	items = titem_dict.items()
	items.sort()
	for key, value in items:
		write2file(match_result_step2, value)


def join_files_by_titem_id():
	menpiao_dict = {}
	for i in range(1, len(open(domestic_menpian_wanle_items, "rU").readlines()) + 1):
		line = linecache.getline(domestic_menpian_wanle_items, i)
		menpiao_dict[line.split('\t')[0].strip()] = line

	for i in range(1, len(open(match_result_step2, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step2, i)
		splid_fields = line.split('\t')
		curr_titem_id = splid_fields[7].strip()
		if curr_titem_id == 'NA':
			content2 = splid_fields[3] + '\t' + 'NA' + '\t' + splid_fields[1] + '\t'
			content2 = content2 + splid_fields[2] + '\t' + '未匹配上' + '\n'
			write2file(match_result_step3, content2)
			continue
		if curr_titem_id in menpiao_dict:
			content = splid_fields[3] + '\t' + splid_fields[5] + '\t' + splid_fields[6] + '\t'
			content = content + splid_fields[2] + '\t' + menpiao_dict[curr_titem_id].split('\t')[2] + '\n'
			write2file(match_result_step3, content)
		else:
			content = splid_fields[3] + '\t' + splid_fields[5] + '\t' + splid_fields[6] + '\t'
			content = content + splid_fields[2] + '\t' + '未匹配上' + '\n'
		# write2file(match_result_step3, content)


def sort_result():
	city_dict = {}
	for i in range(1, len(open(match_result_step3, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step3, i)
		split_fields = line.split('\t')
		city_name = split_fields[0].strip()
		rank = split_fields[3].strip()

		key = city_name + '@@' + rank
		if key not in city_dict:
			city_dict[key] = line
		else:
			city_dict[key] = city_dict[key] + '@@@@' + line

	items = city_dict.items()
	items.sort()
	for key, value in items:
		for line in value.split('@@@@'):
			write2file(match_result_step4, line)


def first_step_match():
	fliggy_scenic_dict = init_fliggy_scenic_data(file_fliggy_scenics_original)

	titem_ids = []
	domestic_names = []
	oversea_names = []

	# header = '马蜂窝城市名称' + '\t' + '马蜂窝景点名称' + '\t' + '马蜂窝景点顺序' + '\t' + '飞猪城市名称' + '\t' + '是否是国外城市'
	# header = header + '\t' + '飞猪景点ID' + '\t' + '飞猪景点名称' + '\t' + '飞猪主商品ID' + '\n'
	# write2file(match_result, header)
	for i in range(1, len(open(file_mafengwo_top_scenics, "rU").readlines()) + 1):
		mafengwo_line = linecache.getline(file_mafengwo_top_scenics, i)
		mafengwo_city_name = mafengwo_line.split('\t')[1].strip()
		mafengwo_scenic_name = mafengwo_line.split('\t')[2].strip()
		mafengwo_scenic_rank = mafengwo_line.split('\t')[3].strip()

		if mafengwo_city_name in fliggy_scenic_dict:
			one_city_fliggy_scenics = fliggy_scenic_dict[mafengwo_city_name]
			fliggy_scenic_split_lines = one_city_fliggy_scenics.split('@@@@')
			matched = False
			is_domestic = True
			for fliggy_scenic_line in fliggy_scenic_split_lines:
				fliggy_titem_id = fliggy_scenic_line.split('\t')[0].strip()
				fliggy_scenic_id = fliggy_scenic_line.split('\t')[1].strip()
				fliggy_scenic_name = fliggy_scenic_line.split('\t')[2].strip()
				fliggy_province_id = fliggy_scenic_line.split('\t')[5].strip()
				fliggy_province_name = fliggy_scenic_line.split('\t')[6].strip()
				fliggy_city_id = fliggy_scenic_line.split('\t')[7].strip()
				fliggy_city_name = fliggy_scenic_line.split('\t')[8].strip()
				fliggy_country_id = fliggy_scenic_line.split('\t')[11].strip()
				fliggy_country_name = fliggy_scenic_line.split('\t')[12].strip()
				# 是否是国外城市
				is_board = 0
				if fliggy_country_id != 'NA' and fliggy_province_id == 'NA':
					is_board = 1
					is_domestic = False

				if is_board == 1:
					continue

				clean_mafengwo_scenic_name = mafengwo_scenic_name.replace(mafengwo_city_name, '')
				clean_fliggy_scenic_name = fliggy_scenic_name.replace(mafengwo_city_name, '')

				if mafengwo_scenic_name in fliggy_scenic_name or fliggy_scenic_name in mafengwo_scenic_name or clean_mafengwo_scenic_name == clean_fliggy_scenic_name:
					content = mafengwo_city_name + '\t' + mafengwo_scenic_name + '\t' + mafengwo_scenic_rank + '\t'
					content = content + fliggy_city_name + '\t' + str(is_board) + '\t' + fliggy_scenic_id + '\t'
					content = content + fliggy_scenic_name + '\t' + fliggy_titem_id + '\n'
					write2file(match_result_step1, content)
					matched = True
			if matched == False and is_domestic == True:
				content = mafengwo_city_name + '\t' + mafengwo_scenic_name + '\t' + mafengwo_scenic_rank + '\t'
				content = content + fliggy_city_name + '\t' + 'NA' + '\t' + 'NA' + '\t'
				content = content + 'NA' + '\t' + 'NA' + '\n'
				write2file(match_result_step1, content)



if __name__ == '__main__':
	file_mafengwo_top_scenics = 'mafengwo_top_scenics.txt'
	file_fliggy_scenics_original = 'fliggy_scenics_original.txt'
	domestic_menpian_wanle_items = 'domestic_menpian_wanle_items.txt'
	match_result_step1 = 'match_result_step1.txt'
	match_result_step2 = 'match_result_step2.txt'
	match_result_step3 = 'match_result_step3.txt'
	match_result_step4 = 'match_result_step4.txt'

	# first_step_match()
	# clean_step1_data()
	# join_files_by_titem_id()
	# sort_result()



	matched_city = {}
	unmatched_city = {}
	for i in range(1, len(open(match_result_step4, "rU").readlines()) + 1):
		line = linecache.getline(match_result_step4, i)
		split_fields = line.split('\t')
		city_name =split_fields[0].strip()
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

		if city_name in matched_city:
			tmp = matched_city[city_name]
			tmp.append(scenic_name)
			matched_city[city_name] = tmp
		else:
			matched_city[city_name] = [scenic_name]

	for k, v in  matched_city.items():
		print k, len(set(v)), len(set(v)) - len(set(unmatched_city[k]))



	# city_name_list = []
	# how_many_scenic = []
	# matched_scenic = {}
	# for i in range(1, len(open(match_result_step4, "rU").readlines()) + 1):
	# 	line = linecache.getline(match_result_step4, i)
	# 	split_fields =  line.split('\t')
	# 	city_name =split_fields[0].strip()
	#
	# 	city_name_list.append(city_name)
	#
	# 	scenic_id = split_fields[1].strip()
	# 	scenic_name = split_fields[2].strip()
	# 	scenic_rank = split_fields[3].strip()
	# 	item_title = split_fields[4].strip()
	#
	# 	how_many_scenic.append(city_name + '@@' + scenic_name)
	#
	# 	key = city_name + '@@' + scenic_name
	# 	if key in matched_scenic:
	# 		matched_scenic[key] = int(matched_scenic[key]) + 1
	# 	else:
	# 		if item_title != '未匹配上':
	# 			matched_scenic[key] = 1
	# print len(set(city_name_list))
	# print len(set(how_many_scenic))
	#
	# for k, v in  matched_scenic.items():
	# 	print k.split()
	#
	# print len(matched_scenic.keys())

