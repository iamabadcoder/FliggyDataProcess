# -*- coding:utf-8 -*-
import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def init_dang_di_wan_le_data(file_name):
	dang_di_wan_le_dict = {}
	for i in range(1, len(open(file_name, "rU").readlines()) + 1):
		line = linecache.getline(file_name, i).strip()
		split_fields = line.split('\t')
		if len(split_fields) != 6:
			print line
		city_name = split_fields[5].strip()
		if city_name in dang_di_wan_le_dict:
			dang_di_wan_le_dict[city_name] = dang_di_wan_le_dict[city_name] + '@@@@' + line
		else:
			dang_di_wan_le_dict[city_name] = line
	return dang_di_wan_le_dict


if __name__ == '__main__':
	file_dang_di_wan_le_items = 'dang_di_wan_le_items.txt'
	file_mafengwo_top_scenics = 'mafengwo_top_scenics.txt'

	file_wan_le_step1 = 'wan_le_step1.txt'

	dang_di_wan_le_dict = init_dang_di_wan_le_data(file_dang_di_wan_le_items)
	print len(dang_di_wan_le_dict)

	for i in range(1, len(open(file_mafengwo_top_scenics, "rU").readlines()) + 1):
		line = linecache.getline(file_mafengwo_top_scenics, i).strip()
		split_fields = line.split('\t')
		mafengwo_city_name = split_fields[1].strip()
		mafengwo_scenic_name = split_fields[2].strip()
		mafengwo_scenic_rank = split_fields[3].strip()

		if mafengwo_city_name in dang_di_wan_le_dict:
			dang_di_wan_le_by_city = dang_di_wan_le_dict[mafengwo_city_name]
			dang_di_wan_le_lines = dang_di_wan_le_by_city.split('@@@@')
			for wan_le_line in dang_di_wan_le_lines:
				id = wan_le_line.split('\t')[0].strip()
				item_id = wan_le_line.split('\t')[1].strip()
				item_title = wan_le_line.split('\t')[2].strip()
				item_province = wan_le_line.split('\t')[4].strip()
				item_city = wan_le_line.split('\t')[5].strip()
				if mafengwo_scenic_name in item_title:
					content = item_city + '\t' + item_id + '\t' + mafengwo_scenic_name + '\t' + mafengwo_scenic_rank + '\t'
					content = content + item_title + '\n'
					write2file(file_wan_le_step1, content)


