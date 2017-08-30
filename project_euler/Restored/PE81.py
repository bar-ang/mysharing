#Completed on Tue, 18 Mar 2014, 10:12

import sys
import numpy as np

file = "p081_matrix.txt"

if len(sys.argv) > 1:
	file = sys.argv[1]

f = open(file,'r')

def loadMatrix(f):
	mat = []
	for line in f.readlines():
		mat.append([])
		for val in line.split(','):
			mat[-1].append(int(val))
	return mat

def getMinimalPathSum(mat, x=0, y= 0, carry = 0):
	if x == len(mat)-1 and y == len(mat[0])-1:
		return carry+mat[x][y]
	#elif x == len(mat)-1:
	#	return getMinimalPathSum(mat, x, y+1, carry+mat[x][y])
	#elif y == len(mat[0])-1:
	#	return getMinimalPathSum(mat, x+1, y, carry+mat[x][y])

	v = mat[x][y]
	downCost = mat[x][y+1]
	rightCost = mat[x+1][y]
	
	if downCost < rightCost:
		return getMinimalPathSum(mat, x, y+1, carry+v)
	else:
		return getMinimalPathSum(mat, x+1, y, carry+v)


mat = loadMatrix(f)

print getMinimalPathSum(mat)