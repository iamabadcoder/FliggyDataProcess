# -*- coding:utf-8 -*-

import os
import subprocess
import linecache
import sys
import time
import json

reload(sys)
sys.setdefaultencoding('utf8')


def mv_files():
	path = "/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/pdf"
	json_file = "/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/accommodation_info.txt"
	new_dir = "/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/pdf_new/"
	dest_list = []
	for i_line_num in range(1, len(open(json_file, 'rU').readlines()) + 1):
		i_line = linecache.getline(json_file, i_line_num)
		json_obj = json.loads(i_line)
		dest_list.append(json_obj['destination'])

	filelist = os.listdir(path)
	for files in filelist:
		old_dir = os.path.join(path, files)
		file_type = os.path.splitext(files)[1]
		file_name = os.path.splitext(files)[0]
		if file_type is not None and 'pdf' in file_type and file_name in dest_list:
			subprocess.Popen(
				'mv ' + '"' + old_dir.encode("utf-8") + '" ' + new_dir, shell=True)

def pdf_2_html():
	path = "/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/pdf"
	filelist = os.listdir(path)
	for files in filelist:
		old_dir = os.path.join(path, files)
		if os.path.isdir(old_dir):
			continue
		file_name = os.path.splitext(files)[0]
		file_type = os.path.splitext(files)[1]
		if file_type is not None and 'pdf' in file_type:
			subprocess.Popen(
				'pdf2htmlEX --dest-dir /Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea --no-drm 1 ' + '"' + old_dir.encode(
					"utf-8") + '"', shell=True)
	time.sleep(600)


if __name__ == '__main__':
	pdf_2_html()
