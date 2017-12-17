from subprocess import Popen, PIPE
import string
import sys
import random
import os


forkevery = 2*10**2

iteron = "anemcbx01239"
literon = list(iteron)

#random.shuffle(literon)

iteron = "".join(literon)

print "iterate on: %s" % iteron

wwwlist = []

#for a in iteron:
#	for b in iteron:
#		for c in iteron:
#			for d in iteron:
#				wwwlist.append("w%s%s.%s%s.ofekangel.com" %(a,b,c,d))
#			wwwlist.append("w%s%s.%s.ofekangel.com" %(a,b,c))
#			wwwlist.append("w%s.%s%s.ofekangel.com" %(a,b,c))
#		wwwlist.append("w%s.%s.ofekangel.com" %(a,b))
#		wwwlist.append("w%s%s.ofekangel.com" %(a,b))
#	wwwlist.append("w%s.ofekangel.com" %(a))


for a in iteron:
	for b in iteron:
		wwwlist.append("ofekangel%s%s.com" %(a,b))
		wwwlist.append("ofekangel-%s%s.com" %(a,b))
		wwwlist.append("ofekangel_%s%s.com" %(a,b))
	wwwlist.append("ofekangel%s.com" %(a))
	wwwlist.append("ofekangel-%s.com" %(a))
	wwwlist.append("ofekangel_%s.com" %(a))



for a in iteron:
	for b in iteron:
		wwwlist.append("%s%sofekangel.com" %(a,b))
		wwwlist.append("%s%s-ofekangel.com" %(a,b))
		wwwlist.append("%s%s_ofekangel.com" %(a,b))
	wwwlist.append("%sofekangel.com" %(a))
	wwwlist.append("%s-ofekangel.com" %(a))
	wwwlist.append("%s_ofekangel.com" %(a))
random.shuffle(wwwlist)

lim = 0

resfile = open("result.txt","w+")

for www in wwwlist:
	lim += 1
	lookfor = www
	process = Popen(['nslookup', lookfor], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()

	if stdout.find("server can't find") < 0 and stderr.find("is not a legal") < 0:
		print "%s - FOUND" % (lookfor)
		print "iterate on %s addresses" % lim
		resfile.write(lookfor + "\n")
		#sys.exit(777)
	else:
		print "%s - nope." % (lookfor,)