import sys, socket, struct, os

subnet = sys.argv[1]
blim = int(sys.argv[2])
ulim = int(sys.argv[3])
port = int(sys.argv[4])
sendstr = sys.argv[5]

TIMEOUT = 5
#example: python IpScanner.py 192.168.1 100 115 9000 $welcome$

def glueSize(s):
	size = len(s)
	return struct.pack(">I",size) + s

def showIP(ans, ip):
	param = ans.split("=")[1]
	print "%s\t\t http://%s:%s" % (param, ip, port)

sendstr = glueSize(sendstr)

sock = socket.socket()
sock.settimeout(TIMEOUT)

print "Be patient! Scanning may take up to %s seconds." % TIMEOUT
print "Device name\tIP Address"
for i in range(blim, ulim+1):
	ip = "%s.%s" % (subnet,str(i))
	res = 0
	if res == 0:
		try:
			sock.connect((ip,port))
		except socket.error, msg:
			print "No IP %s" % ip
			sys.exit(-1)
		#print "connection accepted on IP %s" % ip
		sock.send(sendstr)
		ans = sock.recv(4)
		size = int(struct.unpack(">I", ans)[0])
		ans = sock.recv(size)
		if ans.find("TAUIOT@devname") >= 0:
			showIP(ans, ip)
		else:
			print "but message is not in the right format: %s" % ans
		sock.close()
		sys.exit(0)