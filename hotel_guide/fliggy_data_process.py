# -*- coding:utf-8 -*-

import linecache


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


if __name__ == '__main__':
	fliggy_data_filename = 'fliggy_zone_data.txt'
	fliggy_data_step1 = 'fliggy_zone_data_step1.txt'
	for i in range(1, len(open(fliggy_data_filename, "rU").readlines()) + 1):
		line = linecache.getline(fliggy_data_filename, i)
		field_list = line.split('####')
		if 'NA' in field_list[9] and 'NA' in field_list[10]:
			continue
		content = field_list[3] + '\t' + field_list[9] + '\t' + field_list[10] + '\t' + field_list[0] + '\t' + \
				  field_list[1] + '\n'
		write2file(fliggy_data_step1, content)
