def rootSearch(k,a,b):  #returns the square root of k if it has a natural root in the range [a^2, b^2]. returns None otherwise
	if a > b:
		return None

	m = (a+b)//2
	if k == m*m:
		return m
	elif k > m*m:
		return rootSearch(k,m+1,b)
	else:
		return rootSearch(k,a,m-1)

def getPitagoreans(lim):
	a,b = 1,1
	while b*b <= lim*lim:
		a = 1
		while a <= b:
			c = rootSearch(a*a+b*b,0,lim*lim)
			if c != None:
				print a,b,c
			a += 1
		b += 1

def sumRoutes(lim):
	s = 0
	a,b = 1,1
	while b*b <= lim*lim:
		a = 1
		while a <= b:
			c = rootSearch(a*a+b*b,0,lim*lim)
			if c != None:
				s += a // 2
			a += 1
		b += 1
	return s

def routesToSum(lim):
	s = 0
	a,b = 1,1
	while s <= lim:
		a = 1
		while a <= b:
			c = rootSearch(a*a+b*b,0,lim*lim)
			if c != None:
				s += a // 2
			a += 1
		b += 1
	return b

print routesToSum(10**6)

