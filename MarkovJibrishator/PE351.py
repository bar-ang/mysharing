def blockdivide(n,d):
	res =  n
	while res % d == 0:
		res //= d
	return res


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

f = Factorizator(10**6)
f.factorize()

print f.getFactors(2)
print f.getFactors(3)
print f.getFactors(4)
print f.getFactors(10)
print f.getFactors(60)
print f.getFactors(61)
print f.getFactors(66)
print f.getFactors(987654)