#Completed on Sat, 22 Aug 2015, 03:49

import sys
import numpy as np

N = 100

if len(sys.argv) > 1:
	N = int(sys.argv[1])

dynam = np.zeros((N+1,N+1)).astype(int)

dynam[0,:] = 1

for n in range(1,N+1):
	for k in range(1,N+1):
		if n < k:
			dynam[n,k] = dynam[n,k-1]
		else:
			dynam[n,k] = dynam[n-k,k] + dynam[n,k-1]

print dynam[N,N-1]