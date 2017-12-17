from scapy.all import *
import sys

def action(packet):
	if IP in packet:
		print packet[IP].source

def main(argv):
	sniff(prn = action, timeout = int(argv[6]))

main(sys.argv)