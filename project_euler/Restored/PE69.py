import sys
import math

N = 1000000

if len(sys.argv) > 1:
	N = int(sys.argv[1])

#Note that for two numbers with the exact same prime factors, this ratio will be the same
#Numbers with small prime factors will have a bigger ratio
#So we only need to 'accumalate' primes until their product reaches N

primeprod = 2

for i in range(N):
	m = (int)(math.sqrt(i)+2)
	found = 0
	for q in range(2,m):
		if i % q == 0:
			break
		elif q == m-1:
			primeprod *= i
			found = i
	if primeprod > N:
		primeprod /= found
		break

print primeprod

