import numpy as np

def f(x):
	return 2*x*(x+2)

def g(x):
	return x*(x+1)

brute = 5000
deg = 8
space = 10

A = np.zeros((deg+1,deg+1))
b = np.zeros((deg+1,1))

d=0
for i in range(0,brute):
	for j in range(i,brute):
		if f(i) == g(j):
			print "f(%s) = g(%s) = %s" % (i,j,f(i))
			p = space
			for c in range(deg+1):
				A[d,c] = (j-i)**c
			b[d] = f(i)
			d += 1
		if d > deg:
			break

x = np.linalg.solve(A,b)
print x.astype(int)