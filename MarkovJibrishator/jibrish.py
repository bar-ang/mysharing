import random
import re

class LetterJibberish(object):
 	"""docstring for ClassName"""
 	def __init__(self, order):
 		self.text = None
 		self.order = order
 		self.graph = {}

	def cleanText(self, text):
		text = text.lower()
		out = ""
		for c in text:
			if (ord(c) >= ord("a") and ord(c) <= ord("z")):
				out += c
		return out

 	def train(self, inputfile):
 		self.text = open(inputfile,'r').read()
 		self.text = self.text + self.text[:self.order]
 		self.text = self.cleanText(self.text)
 		for i in range(len(self.text) - self.order - 1):
 			key = tuple(self.text[i:i + self.order])
 			value = self.text[i + self.order]
 			if key in self.graph:
 				self.graph[key].append(value)
 			else:
 				self.graph[key] = [value]

 	def generate(self, maxlength):
 		index = random.randint(0,len(self.text) - self.order)
 		#while self.text[index] == " ":
 		#	index = random.randint(0,len(self.text) - self.order)
 		result = tuple(self.text[index:index + self.order])
 		for i in range(maxlength):
 			state = result[len(result) - self.order:]
 			next_letter = random.choice(self.graph[state])
 			if next_letter == " ":
 				break
 			result += (next_letter,)

 		return "".join(result[self.order:])

#for i in range(0,200,5):
#	lj = LetterJibberish(i)
#	lj.train("train.txt")
#	print lj.generate(13)

lj = LetterJibberish(30)
lj.train("train.txt")

words = []
for i in range(200):
	w = lj.generate(6)
	while len(w) < 2:
		w = lj.generate(15)
	words.append(w)
print " ".join(words)