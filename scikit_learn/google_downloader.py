import requests 
import lxml.html 
import sys
import os

import urllib2


def clean(string):
	string = string.lower()
	string= string.replace(" ","_")
	return string

folder = sys.argv[1]
search = sys.argv[2]
count = int(sys.argv[3])

URL = """https://www.google.co.il/search?q=%s&client=ubuntu&hs=ASH&channel=fs&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjJt8OUmsvVAhVpDcAKHQkcCgQQ_AUICigB&biw=1403&bih=758"""



r = requests.get(URL % search) 


doc = lxml.html.fromstring(r.content)
c = 0
for t in doc.xpath("""//div[@id="ires"]//img/@src"""):
	res = urllib2.urlopen(t)
	pic = res.read()
	f = open("%s/%s%s.jpg" % (folder,clean(search),c),"w+")
	f.write(pic)
	c += 1
	if c >= count:
		print "stopped"
		break