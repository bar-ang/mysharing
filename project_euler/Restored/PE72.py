import sys
import euler_tools as euler
N = 1000000

if len(sys.argv) > 1:
	N = int(sys.argv[1])

nt = euler.NumberTheory(N+1)

nt.getminfactors()

s = 0
for n in range(2,N+1):
	print "%s->%s" % (n,nt.minfactors[n])

print s