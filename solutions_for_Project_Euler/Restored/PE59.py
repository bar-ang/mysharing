#Completed on Fri, 14 Mar 2014, 23:57

import sys

COMMON_WORDS = ['a ','the ','and ', 'is ',' ']
FORBIDDEN_CHARS = "$%&*@#<>~"
def textify(ascii):
	s = ""
	for c in ascii:
		s += chr(c)
	return s

def check_semantics(text, common_words = COMMON_WORDS, tolerance = 1):
	eng = 0
	for c in FORBIDDEN_CHARS:
		if c in text:
			return False

	for word in common_words:
		if text.find(word) >= 0 :
			eng += 1
	if eng > tolerance:
		return True
	else:
		return False


def tryKey(ascii, key, keysize = 3):
	dec = []
	keyloc = 0
	for c in ascii:
		dec.append(c^key[keyloc])
		keyloc += 1
		if keyloc >= keysize:
			keyloc = 0
	return dec

def decipher(cipher):
	for i in range(ord('a'), ord('z')+1):
		for j in range(ord('a'), ord('z')+1):
			for k in range(ord('a'), ord('z')+1):
				decipher = tryKey(cipher,[i,j,k])
				if check_semantics(textify(decipher)):
					return decipher
	return None

def loadData(filename):
	f = open(filename,'r')
	asci = []
	for c in f.read().split(','):
		asci.append(int(c))
	return asci


cipher = loadData(sys.argv[1])

dec = decipher(cipher)
if dec == None:
	print "could not decipher"
	sys.exit(0)
print textify(dec)
print "ANSWER: %s" % sum(dec)
