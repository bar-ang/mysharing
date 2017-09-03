def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b.

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """
    while b:
        a, b = b, a%b
    return a

def fast_power_modulo(n,k,d):
	"""
		calculates (n**k mod d)
		where '**' denotes the power operation
		e.g. 2^10 mod 10 = 24
	"""
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

def fast_power(n,k):
	"""
		calculates n**k
		where '**' denotes the power operation
		e.g. 2^10 = 1024
	"""
	if k == 0:
		return 1
	r = 1
	m = n
	while r*2 <= k:
		m *= m
		r *= 2
	ans = m*fast_power_modulo(n,k-r)
	return ans


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


def factorize_all(N, with_oders=True):
	"""
		returns a dictionary that contains a key for each integer in the range [2,N]
		and the value for key 'k' is the canonical form of k.
	"""
	factors = {}
