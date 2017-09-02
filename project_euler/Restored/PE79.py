from Queue import *
import sys


file = "p079_keylog.txt"

if len(sys.argv) > 1:
	file = sys.argv[1]

q = Queue()

def get_most_frequent(lst, r=10):
	accum = [0]*r
	for x in lst:
		accum[x] += 1
	m = max(accum)
	maxes = []
	for i in range(r):
		if accum[i] == m and not i in maxes:
			maxes.append(i)
	return maxes


def harvest_queues(queues):
	har = []
	for q in queues:
		if len(q) > 0:
			har.append(q[0])
	return har

def clean(queues):
	for q in queues:
		if len(q) == 0:
			queues.remove(q)
			clean(queues)
			break

def clone(queues):
	n = []
	for q in queues:
		n.append(q[:])
	return n

def pop_all(queues,val):
	for q in queues:
		if len(q) > 0 and q[0] == val:
			q.pop(0)
	clean(queues)

def loadData(filename):
	f = open(filename,'r')
	queues = []
	for line in f.readlines():
		q = []
		q.append(int(line[0]))
		q.append(int(line[1]))
		q.append(int(line[2]))
		queues.append(q)
	return queues

def findCode(queues):
	if len(queues) == 0:
		return ""
	most_common = get_most_frequent(harvest_queues(queues))
	mincode = None
	minv = None
	for v in most_common:
		nextq = clone(queues)
		pop_all(nextq,v)
		code = findCode(nextq)
		if mincode == None or len(code) <= len(mincode):
			mincode = code
			minv = v
	return str(minv) + mincode

queues = loadData(file)
k = clone(queues)
code = findCode(k)

print code


