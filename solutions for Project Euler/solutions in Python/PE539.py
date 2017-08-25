def simulate(n):
	lst = list(range(1,n+1))
	lst.reverse()
	while len(lst) > 1:
		lst = lst[-2::-2]
	if len(lst) > 0:
		return lst[0]
	else:
		return None

def segment_2(k):
	p = 0
	lseg = 1
	rseg = 2
	res = {}

	choose = 1
	res[1] = 0
	for i in range(0,k+1):
		if choose == 1:
			lseg = rseg
		rseg = lseg + 2**(i+1)
		choose = 1 - choose
		res[2**(i+1)] = lseg
	return res

for i in range(0,1000,2):
	s = simulate(i)
	if s == 502:
		print "P(%s) = %s" % (i, s)