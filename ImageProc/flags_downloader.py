import sys
import os

domain = "http://www.flagid.org/flagfiles/"
suffix = ".gif"
folder = "flags"
count = 1285

if len(sys.argv) > 1:
	folder = sys.argv[1]

if not os.path.exists(folder):
	os.makedirs(folder)

for i in range(count):
 	scount = str(i)
 	com = "curl -o %s/flag_%s%s %s%s%s" % (folder,scount,suffix,domain,scount,suffix)
 	print com
 	os.system(com)