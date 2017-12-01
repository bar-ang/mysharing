from scapy.all import *

MY_IP = "192.168.1.104"

def filt(pack):
	return IP in pack and pack[IP].src == MY_IP

def action(pack):
	print "%s ==> %s" % (pack[IP].src,pack[IP].dst)

sniff(lfilter=filt, prn=action)