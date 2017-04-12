# -*- coding:utf-8 -*-

import time
import json
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
	ajax_url = 'http://www.tripadvisor.cn/CityGuideAjax?action=list&c=0&sortOrder=1'
	request_ajax_url = requests.get(ajax_url)
	if request_ajax_url.status_code != 200:
		print 'request error!!!'

	res_json_obj = json.loads(request_ajax_url.text.replace('while(1);', ''))
	for city_guide in res_json_obj['cityGuideList']:
		download_url = city_guide['downloadUrl']
		detail_url = city_guide['detailUrl']
		cover_name = city_guide['coverName']
		time.sleep(4)
		request_download_url = requests.get('http://www.tripadvisor.cn' + str(download_url))
		while request_download_url.status_code != 200:
			print cover_name
			continue
		print '开始下载:' + str(cover_name)
		with open(cover_name + '.pdf', 'wb') as f:
			for chunk in request_download_url.iter_content(chunk_size=1024):
				if chunk:
					f.write(chunk)
					f.flush()
