def blockdivide(n,d):
	res =  n
	while res % d == 0:
		res //= d
	return res

def sieve(n):
	primes = []
	notPrimes = []
	for p in range(2,n+1):
		if p in notPrimes:
			continue
		primes.append(p)
		for n in range(2*p,n+1,p):
			notPrimes.append(n)
	return primes

def primes2(n):
    """ Input n>=6, Returns a list of primes, 2 <= p < n """
    n, correction = n-n%6+6, 2-(n%6>1)
    sieve = [True] * (n/3)
    for i in xrange(1,int(n**0.5)/3+1):
      if sieve[i]:
        k=3*i+1|1
        sieve[      k*k/3      ::2*k] = [False] * ((n/6-k*k/6-1)/k+1)
        sieve[k*(k-2*(i&1)+4)/3::2*k] = [False] * ((n/6-k*(k-2*(i&1)+4)/6-1)/k+1)
    return [2,3] + [3*i+1|1 for i in xrange(1,n/3-correction) if sieve[i]]

class Factorizator(object):
	"""docstring for Factorization"""
	def __init__(self, until):
		self.until = until
		self.factors = {}
		self.isInit = False

	def factorize(self):
		leftovers = list(range(0,self.until+1))
		
		for p in range(2,len(leftovers)):
			if leftovers[p] == 1:
				continue
			for i in range(p,len(leftovers),p):
				if i in self.factors: 
					self.factors[i].append(p)
				else:
					self.factors[i] = [p]
				leftovers[i] = blockdivide(leftovers[i],p)

	def getFactors(self,n):
		return tuple(self.factors[n])

def comb(primes, lim):
	if len(primes) == 1:
		return [1]
	lst = mobius(primes[1:], lim)
	explst = [primes[0]*x for x in lst]
	return lst + explst


def mobius(primes, lim):
	if len(primes) == 0:
		return 0
	if len(primes) == 1:
		return primes[0]
	m = mobius(primes[1:], lim)
	return (primes[0]+1)*m 

print "start"
primes = primes2(10**1)
print "sieved"
#print primes
m = mobius(primes,100)
print m
#f = Factorizator(10**6)
#f.factorize()
