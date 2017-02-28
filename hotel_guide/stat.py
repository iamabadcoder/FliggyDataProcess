# -*- coding:utf-8 -*-

import os
import sys
import linecache

reload(sys)
sys.setdefaultencoding('utf8')

def find_lcsubstr(s1, s2):
	m = [[0 for i in range(len(s2) + 1)] for j in range(len(s1) + 1)]
	mmax = 0  # 最长匹配的长度
	p = 0  # 最长匹配对应在s1中的最后一位
	for i in range(len(s1)):
		for j in range(len(s2)):
			if s1[i] == s2[j]:
				m[i + 1][j + 1] = m[i][j] + 1
				if m[i + 1][j + 1] > mmax:
					mmax = m[i + 1][j + 1]
					p = i + 1
	return s1[p - mmax:p], mmax  # 返回最长子串及其长度

if __name__ == '__main__':
	print find_lcsubstr(u'蝴蝶泉', u'下波淜村')[0], find_lcsubstr(u'蝴蝶泉', u'下波淜村')[1]

'''
# city_list = []
# file_name = './haoqiao_final_result.txt'
# for ith in range(1, len(open(file_name, 'rU').readlines()) + 1):
# 	ith_line = linecache.getline(file_name, ith)
# 	fields_list = ith_line.split('\t')
# 	city_list.append(fields_list[0])
# print len(set(city_list))
'''
