import sys
import euler_tools as euler
N = 100

if len(sys.argv) > 1:
	N = int(sys.argv[1])


r = euler.sieve(N*(N+1)//2)
print "printing.."
