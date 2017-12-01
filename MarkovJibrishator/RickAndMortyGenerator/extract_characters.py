import sys
import re
import os

def loadFile(filename):
	return open(filename, 'r').read().lower()

def extractCharacters(text):
	quotes = {}

	divider = re.compile(r'\w+:.*')
	sayings = divider.findall(text)

	for saying in sayings:
		p = saying.split(":")
		if p[0] in quotes.keys():
			quotes[p[0]].append(p[-1])
		else:
			quotes[p[0]] = [p[-1]]

	return quotes

def saveCharacter(filename, lst):
	f = open(filename,'w')
	for sent in lst:
		f.write(sent + "\n")


if len(sys.argv) <= 1:
	print "please choose a file for training."
	sys.exit()

text = loadFile(sys.argv[1])

chars = extractCharacters(text)


if not os.path.exists("characters"):
    os.makedirs("characters")

for char in chars:
	saveCharacter("characters/" + char + ".dubdub", chars[char])