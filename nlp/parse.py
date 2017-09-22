from __future__ import division  # Python 2 users only
import nltk, re, pprint
from nltk import word_tokenize,sent_tokenize
from nltk.corpus import brown

text = open("trump.txt","r").read()

sents = sent_tokenize(text)
for sent in sents:
	print "[%s]" % tagged_words(sent)

print text1.generate()