import sys, os

def getGCDMatrix(m):
	mat = [[1 for j in range(m+1)] for i in range(m+1)]
	for i in range(m+1):
		for j in range(i,m+1):
			if i == j or i == 0:
				if j != 1:
					mat[i][j] = 0
					mat[j][i] = 0
				continue
			if mat[i][j] != 1:
				continue
			r = 2
			while r*i <= m and r*j <= m:
				mat[r*i][r*j] = 0		
				mat[r*j][r*i] = 0
				r += 1
	return mat

def calculate_P_Raw(a,b):
	a,b = min(a,b), max(a,b)
	acc = 0
	f = float(b)/float(a)
	for i in range(1,a):
		acc += int(float(b)-f*float(i))
	return acc

def calulate_P(m, gcdm):
	P = {}
	for i in range(1,m+1):
		for j in range(i,m+1):
			s = calculate_P_Raw(i,j)
			#P[(i,j)] = s
			#P[(j,i)] = s
			if gcdm[i][j] == 1:
				s = calculate_P_Raw(i,j)
				P[(i,j)] = s
				P[(j,i)] = s
				r = 2
				while r*i <= m and r*j <= m:
					P[(r*i,r*j)] = s*r + r*(r-1)*i*j/2
					P[(r*j,r*i)] = s*r + r*(r-1)*i*j/2
					r += 1

	return P

def listSquares(m):
	s = 1
	sqrs = []
	while s*s <= m:
		sqrs.append(s*s)
		s += 1
	return sqrs


def combine(P,a,b,c,d):
	return P[(a,b)] + P[(b,c)] + P[(c,d)] + P[(d,a)] + a + b + c + d - 3

def differ(arr):
	seen = []
	for a in arr:
		if not a in seen:
			seen.append(a)
	return len(seen)


def countSquares(P,m, sqrs):
	count = 0
	for a in range(1,m+1):
		for b in range(1,a+1):
			for c in range(1,a+1):
				for d in range(1,b+1):
					comb = combine(P,a,b,c,d)
					if comb in sqrs:
						if a == b == c == d: #square
							print "square"
							count += 1
						elif a == b and c == d: #rhombus
							print "rhombus"
							count += 2
						elif a == b or c == d: #kite
							print "kite"
							count += 4
						else:
							print "none"
							count += 8

	return count

print "start"

m = 4

gcdm = getGCDMatrix(m)

sqrs = listSquares(50*m)

P = calulate_P(m, gcdm)
print "P is Set!"
#print calculate_P_Raw(3,2)

#print calculate_P_Raw(126,7)

result = countSquares(P,m, sqrs)

print result



def _countSquares(P,m, sqrs):
	count = 0
	for a in range(1,m+1):
		for b in range(1,m+1):
			for c in range(1,a):
				for d in range(1,b):
					comb = combine(P,a,b,c,d)
					if comb in sqrs:
						count += 4

	for a in range(1,m+1):
		for b in range(1,m+1):
			for d in range(1,b):
				comb = combine(P,a,b,a,d)
				if comb in sqrs:
					count += 2

	for a in range(1,m+1):
		for b in range(1,m+1):
			for c in range(1,a):
				comb = combine(P,a,b,c,b)
				if comb in sqrs:
					count += 2

	for a in range(1,m+1):
		for b in range(1,m+1):
			comb = combine(P,a,b,a,b)
			if comb in sqrs:
				count += 1
	return count