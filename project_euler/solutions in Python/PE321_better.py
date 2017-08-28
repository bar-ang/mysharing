import sys

def M(n):
	return n*(n+2)
def tri(t):
	return t*(t+1)//2

tris = []
last_t = 0
def add_to_tri_list(until):
	global last_t
	while tri(last_t) < until:
		tris.append(tri(last_t))
		last_t += 1


def get_bound(k):
	return 2*k*(4*k+1)

n = int(sys.argv[1])


s = 0
c = 0
k = 1
while c < n:
	add_to_tri_list(get_bound(2+k))
	if M(k) in tris:
		c += 1
		s += k
		print "%s. %s => %s" % (c,k,M(k))
	k += 1
print "answer: %s" % s
