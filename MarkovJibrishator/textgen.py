import random
import re

class WordJibberish(object):
 	"""docstring for ClassName"""
 	def __init__(self, order):
 		self.text = None
 		self.order = order
 		self.graph = {}

 	def cleanText(self, text):
		newtext = []
		for word in text:
			out = ""
			for c in word.lower():
				if (ord(c) >= ord("a") and ord(c) <= ord("z")):
					out += c
			if len(word) >= 1:
				newtext.append(out)
		return newtext

 	def train(self, inputfile):
 		self.text = open(inputfile,'r').read().split()
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
 		result = tuple(self.text[index:index + self.order])
 		for i in range(maxlength):
 			state = result[len(result) - self.order:]
 			if state in self.graph:
 				next_word = random.choice(self.graph[state])
 				result += (next_word,)
 		return " ".join(result[self.order:])


 			


wj = WordJibberish(2)
wj.train("rick.txt")

print  wj.generate(100)