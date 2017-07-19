import sys
import os
import subprocess
import re

def main(argv):
	gateway_ip = ''
	gateway_mac = ''
	my_mac = ''

	p = subprocess.Popen(["ip","route"], stdout=subprocess.PIPE)
	res, err = p.communicate()
	matches = re.search(r"default via \d+.\d+.\d+.\d+", res)
	gateway_ip = matches.group().split(' ')[-1]

	p = subprocess.Popen(["arp","-n"], stdout=subprocess.PIPE)
	res, err = p.communicate()
	matches = re.search(r"%s\s+ether\s+[0-9a-f:]{17}" % gateway_ip, res)
	gateway_mac = matches.group().split(' ')[-1]

	p = subprocess.Popen(["ifconfig"], stdout=subprocess.PIPE)
	res, err = p.communicate()
	matches = re.search(r"ether\s+[0-9a-f:]{17}", res)
	my_mac = matches.group().split(' ')[-1]
	cmd = "python NetBlock.py %s %s %s %s %s" % (argv[1], argv[2], my_mac, gateway_mac, gateway_ip)
	os.system(cmd)


main(sys.argv)