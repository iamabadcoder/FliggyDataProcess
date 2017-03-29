# -*- coding:utf-8 -*-

import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')

def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()

if __name__ == '__main__':
	file_mafengwo_top_scenics = 'mafengwo_top_scenics.txt'
	file_mdd_oversea = 'mdd_oversea.txt'
	file_mafengwo_oversea_scenics = 'mafengwo_oversea_scenics.txt'

	oversea_mdd_origin = []
	result_oversea_mdd = []
	for i in range(1, len(open(file_mdd_oversea, "rU").readlines()) + 1):
		line = linecache.getline(file_mdd_oversea, i)
		oversea_mdd_origin.append(line.strip())

	for i in range(1, len(open(file_mafengwo_top_scenics, "rU").readlines()) + 1):
		line = linecache.getline(file_mafengwo_top_scenics, i)
		if line.split('\t')[1].strip() in oversea_mdd_origin:
			result_oversea_mdd.append(line.split('\t')[1].strip())
			write2file(file_mafengwo_oversea_scenics, line)

	print len(set(result_oversea_mdd))