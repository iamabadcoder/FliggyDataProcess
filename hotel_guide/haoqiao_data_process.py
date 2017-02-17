# -*- coding:utf-8 -*-

import re
import sys
import json
import linecache

reload(sys)
sys.setdefaultencoding('utf8')


def write2file(file_name, content):
	file_object = open(file_name, 'a')
	file_object.write(content)
	file_object.close()


def falt_json_data(data_line):
	field_list = data_line.split(',')
	for i in range(len(field_list)):
		if i == 1:
			country_name = field_list[i]
		elif i == 2:
			country_link = field_list[i]
		elif i == 3:
			city_name = field_list[i]
		elif i == 4:
			city_link = field_list[i]
		elif i >= 5:
			zone_info = ','.join(field_list[5:len(field_list)])
			break
	for zone in json.loads(zone_info)['zoneInfo']:
		zone_desc = None
		for key in zone:
			if 'zoneNameCh' in key:
				zone_name_ch = zone['zoneNameCh']
			elif 'zoneDesc' in key:
				zone_desc = zone['zoneDesc']
			if zone_desc is not None:
				search_res = re.search(ur'(\d+%) 的游客选择住这里', unicode(zone_desc), re.S)
				if search_res:
					select_ratio = search_res.group(1)
				else:
					select_ratio = '0%'
		write2file(setp1_file_name,
				   country_name + '\t' + country_link + '\t' + city_name + '\t' + city_link + '\t' + zone_name_ch + '\t' + select_ratio + '\n')


if __name__ == '__main__':
	source_file_name = 'haoqiao_hotel_guide_data_from_odps.txt'
	setp1_file_name = 'haoqiao_hotel_guide_data_setp1.txt'

	# 将JSON数据转换成二维表形式
	# for i in range(1, len(open(source_file_name, "rU").readlines()) + 1):
	# 	line = linecache.getline(source_file_name, i)
	# 	falt_json_data(line)

	haoqiao_cities = []
	for i in range(1, len(open(setp1_file_name, "rU").readlines()) + 1):
		line = linecache.getline(setp1_file_name, i)
		haoqiao_cities.append(line.split('\t')[2])
	haoqiao_cities = list(set(haoqiao_cities))
	print len(haoqiao_cities)

	fliggy_cities = []
	fliggy_data_filename = 'fliggy_zone_data.txt'
	for i in range(1, len(open(fliggy_data_filename, "rU").readlines()) + 1):
		line = linecache.getline(fliggy_data_filename, i)
		city_name = line.split('####')[10]
		if 'NA' in city_name:
			continue
		fliggy_cities.append(city_name.strip())
	fliggy_cities = list(set(fliggy_cities))
	print len(fliggy_cities)

	cities_mapping_dict = {'纽约': '纽约(纽约州)', '芝加哥': '芝加哥 (伊利诺伊州)', '华欣': '华欣/七岩', '兰塔岛': '兰塔岛 (甲米)', '胡志明': '胡志明市',
						   '旧金山': '旧金山 (加利福尼亚州)', '圣托里尼': '圣托里尼岛', '安塔利亚': '安塔丽亚', '温哥华': '温哥华(BC)',
						   '奥兰多': '奥兰多 (佛罗里达州)', '拉斯维加斯':'拉斯维加斯 (内华达州)', '洛杉矶':'洛杉矶 (加利福尼亚州)', '毛里求斯':'毛里求斯岛'
						   ,'长滩岛':'长滩岛, 菲律宾','阳朔':'阳朔县','克拉科夫':'克拉科夫 (克拉科)','罗托鲁阿':'罗吐鲁阿', '米克诺斯岛':'米科诺斯','垦丁':
						   '屏东县','米克诺斯岛':'米克诺斯'}

	count = 0
	for city in haoqiao_cities:
		if city not in fliggy_cities:
			if cities_mapping_dict.get(city) not in fliggy_cities:
				print city
				count += 1
	print count
