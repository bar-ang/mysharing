import sys

N = 100

if len(sys.argv) > 1:
	N = int(sys.argv[1])

def sieve(N):
	cands = list(range(2,N+1))
	primes = []

	while len(cands) > 0:
		p = min(cands)
		primes.append(min(cands))
		for i in cands:
			if i % p == 0:
				cands.remove(i)
	return primes


r = sieve(N*(N+1)//2)
print "printing.."
