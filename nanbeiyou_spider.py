# -*- coding:utf-8 -*-

import re
import sys
import json
import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


if __name__ == '__main__':
	file_feature_info = 'feature_info1.txt'
	prefix_url = 'http://www.nanbeiyou.com/features/all_009006_'
	for i_page in range(101, 201):
		print i_page
		target_url = prefix_url + str(i_page)
		res = requests.get(target_url)
		if res.status_code != 200:
			print 'Error when requests url:' + target_url
		soup = BeautifulSoup(res.content, 'lxml')
		div_list = soup.find_all('div', 'list')[0]
		if div_list is None:
			print 'Error when requests url:' + target_url + ',div_listl is None'
		for a_ele in div_list.find_all('a'):
			feature_name = a_ele.string.strip()
			feature_url = 'http://www.nanbeiyou.com' + a_ele['href']
			feature_res = requests.get(feature_url)
			if feature_res.status_code != 200:
				print 'Error when requests feature_url:' + feature_url
			feature_soup = BeautifulSoup(feature_res.content, 'lxml')
			all_ps = feature_soup.find(id='feature_contant').find_all('p')
			feature_content = ''
			for p in all_ps:
				feature_content = feature_content + p.text.strip()
			content = feature_name + '\t\t\t\t' + feature_content + '\n'
			write2file(file_feature_info, content)
