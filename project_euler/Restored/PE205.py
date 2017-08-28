# Completed on Fri, 19 Feb 2016, 19:08

import sys
import numpy as np

def movementMatrix(n,l,r):
	d = r-l+1
	M = np.zeros((n*d,n*d))
	for i in range(n*d):
		for j in range(max(i-r,0),i-l+1):
			M[i,j] = 1
	return np.matrix(M)

def distribution(n,l,r):
	M = movementMatrix(n,l,r)
	D = np.linalg.matrix_power(M,n-1)
	d = r-l+1
	p = np.zeros((n*d,1))
	p[0:d] = np.ones((d,1))
	rho = D*p 
	rho *= (1.0/(d**n))
	return rho

def computeSuccessProb(d1,d2):
	s = 0
	for k in range(len(d1)):
		for t in range(k+1,len(d2)):
			s += d1[k,]*d2[t,]
	return s[0,0]



pyr = distribution(9,1,4)
cube = distribution(6,1,6)

s = computeSuccessProb(cube, pyr)

print s