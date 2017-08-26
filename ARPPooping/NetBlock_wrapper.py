import sys
import os
import subprocess
import re

def main(argv):

	if len(argv) < 3 or "-help" in argv:
		print "Usage:"
		print "python NetBlock_wrapper.py <IP to block> <Page to send> [<Script file path>]"
		sys.exit(1)

	gateway_ip = ''
	gateway_mac = ''
	my_mac = ''

	nb_path = "NetBlock.py"
	if len(argv) >= 4:
		nb_path = argv[3]

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
	matches = re.search(r"HWaddr\s+[0-9a-f:]{17}", res)
	my_mac = matches.group().split(' ')[-1]
	cmd = "python %s %s %s %s %s %s" % (nb_path, argv[1], argv[2], my_mac, gateway_mac, gateway_ip)
	os.system(cmd)


main(sys.argv)