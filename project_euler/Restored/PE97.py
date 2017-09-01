import sys
from time import *

N = 7830457
K = 28433

if len(sys.argv) > 1:
	N = int(sys.argv[1])

if len(sys.argv) > 2:
	N = int(sys.argv[2])

def fast_power_modulo(n,k,d):
	if k == 0:
		return 1
	r = 1
	m = n
	while r*2 <= k:
		m *= m
		m %= d
		r *= 2
	ans = m*fast_power_modulo(n,k-r,d)
	return ans % d

ten10 = 10**10
p = fast_power_modulo(2,N,ten10)
p *= K
p %= ten10
print p