# -*- coding:utf-8 -*-

import os
import subprocess
import sys
import time

reload(sys)
sys.setdefaultencoding('utf8')


def pdf_2_html():
	path = "/Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/pdf"
	filelist = os.listdir(path)
	for files in filelist:
		old_dir = os.path.join(path, files)
		if os.path.isdir(old_dir):
			continue
		# file_name = os.path.splitext(files)[0]
		file_type = os.path.splitext(files)[1]
		if file_type is not None and 'pdf' in file_type:
			subprocess.Popen(
				'pdf2htmlEX --dest-dir /Users/caolei/PyWorkSpace/FliggyDataProcess/tripadvisor/oversea/html --no-drm 1 ' + '"' + old_dir.encode(
					"utf-8") + '"', shell=True)
	time.sleep(600)


if __name__ == '__main__':
	pdf_2_html()
