# Completed on Fri, 19 Feb 2016, 19:08

import sys
import numpy as np

def movementMatrix(n,d):
	M = np.zeros((n*d,n*d))
	for i in range(n*d):
		for j in range(max(i-d+1,0),i+1):
			M[i,j] = 1
	return np.matrix(M)

def dist(n,d):
	M = movementMatrix(n,d)
	D = np.linalg.matrix_power(M,n-1)
	rho = M*np.ones((n*d,1))
	rho *= (1.0/(d**n))
	print rho
	return rho

print sum(dist(2,6))
