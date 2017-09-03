import sys
from time import *

import euler_tools as tools


N = 7830457
K = 28433

if len(sys.argv) > 1:
	N = int(sys.argv[1])

if len(sys.argv) > 2:
	N = int(sys.argv[2])

ten10 = 10**10
p = tools.fast_power_modulo(2,N,ten10)
p *= K
p %= ten10
print p