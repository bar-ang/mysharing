#Completed on Mon, 20 Jul 2015, 13:18
import sys
from math import *
import euler_tools as tools

x = (3,7)
N = 1000000

if len(sys.argv) > 1:
	vals = sys.argv[1].split('/')
	x = int(vals[0]),int(vals[1])

if len(sys.argv) > 2:
	N = int(sys.argv[2])


def get_mid(d,x,y):
	lam1 = ceil(d*x[0]*1.0/x[1])
	lam2 = floor(d*y[0]*1.0/y[1])

	if d*x[0] % x[1] == 0:
		lam1 += 1
	if d*y[0] % y[1] == 0:
		lam2 -= 1

	if lam2 < lam1:
		return None
	else:
		l = int(lam2)
		m = tools.gcd(l,d)
		return (l/m,d/m)

closest = (0,1)

for d in range(1,N+1):
	v = get_mid(d,closest,x)
	if v != None:
		closest = v
print "Fraction as ('num','denom'): (%s, %s)" % closest