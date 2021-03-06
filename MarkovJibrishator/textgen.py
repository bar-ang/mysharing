import sys
import random
import re

class WordJibberish(object):
 	"""docstring for ClassName"""
 	def __init__(self, order):
 		self.text = None
 		self.order = order
 		self.graph = {}

 	def cleanText(self):
 		text = self.text.lower()
 		regex = re.compile(r'[^a-zA-Z0-9\s]')
 		doublewhite = re.compile(r'\s\s+')
 		newline = re.compile(r'\n')
		res = regex.sub('', text)
		res = newline.sub(' ', res)
		res = doublewhite.sub(r' ', res)
		self.text = res


	def loadFile(self, inputfile, clean = True):
		self.text = open(inputfile,'r').read()
		if clean:
			self.cleanText()



 	def train(self):
 		self.text = self.text.split()
 		self.text = self.text + self.text[:self.order]
 		for i in range(len(self.text) - self.order - 1):
 			key = tuple(self.text[i:i + self.order])
 			value = self.text[i + self.order]
 			if key in self.graph:
 				self.graph[key].append(value)
 			else:
 				self.graph[key] = [value]

 	def generate(self, maxlength):
 		index = random.randint(0,len(self.text) - self.order)
 		result = tuple(self.text[index:index + self.order])
 		for i in range(maxlength):
 			state = result[len(result) - self.order:]
 			if state in self.graph:
 				next_word = random.choice(self.graph[state])
 				result += (next_word,)
 		return " ".join(result[self.order:])


if len(sys.argv) <= 1:
	print "please choose a file for training."
	sys.exit()

order = 2
length = 100

if len(sys.argv) > 2:
	order = int(sys.argv[2])
if len(sys.argv) > 3:
	length = int(sys.argv[3])


wj = WordJibberish(order)
wj.loadFile(sys.argv[1])
wj.train()

print  wj.generate(length)
