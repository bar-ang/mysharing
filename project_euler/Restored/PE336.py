# Completed on Sun, 7 Aug 2016, 19:12

import sys
import string

N = 11
E = 2011

if len(sys.argv) > 1:
	N = int(sys.argv[1])

if len(sys.argv) > 2:
	E = int(sys.argv[2])

def reverse(lst, i):
	revlst = lst[::-1]
	return lst[:i]+revlst[:len(lst)-i]

def getMaximix(nj_level=N-1, root=string.ascii_uppercase[:N]):
	if nj_level == 0:
		return [root]
	if nj_level == len(root)-1:
		return getMaximix(nj_level = nj_level - 1,  root=reverse(root, nj_level-1))

	flipped = reverse(root,nj_level-1)
	maxes = []
	for i in range(nj_level,len(root)-1):
		maxes += getMaximix(nj_level = nj_level - 1,  root=reverse(flipped, i))

	return maxes

maxes = getMaximix()
maxes.sort()

print maxes[E-1]
