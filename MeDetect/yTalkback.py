#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests 
import lxml.html 
import random
import sys, os, time
import pickle
import re

url = """http://www.ynet.co.il/Ext/App/TalkBack/CdaViewOpenTalkBack/0,11382,L-4998326-%s,00.html"""

fwrite = open("talk.csv",sys.argv[1])

for i in range(1,6):
	os.system("""curl -o pride.html "%s" """ % (url % i))

	time.sleep(2)

#r = requests.get(url + page)
	htmlfile = open("pride.html","r")
	doc = lxml.html.fromstring(htmlfile.read())
	htmlfile.close()
	results = doc.xpath("""//div[@id = 'titleDiv']/text()""")
	

	for t in results:
		num = re.search(r"""\d+\.""", t).group()
		t = t.replace(num,"")[1:].replace(",","@@")
		fwrite.write(t.encode("utf-8") + "\n")
		