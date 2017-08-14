#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

EMOJI = ["👍","😪","😅","🤣","😀","😅","🤔","😜","✨","🌚",
	"😅","😳","😶","🤔","🤣","😺","😗","😛",
	"😬","😂"]

ASCII_EMOJI = [":)",":(",":-)",":-(",";-)",";-(","=[","=]",
	":D",":S",":X",":O"]

PUNCTUATION = [".","..","...",
	",",":",";","~","$","%","'","/","^","&"
	"(",")",
	"[","]",]
PUNCTUATION_STR = ".,:;~$%'/\\^&()[]\{\}?!#\""
def  metadata(text): #TODO: problems :(
	#text length
	#No of lines
	#No of words
	#Maximum word length
	words = len(text.split(" "))*1.0
	p = re.search(r"""[.,?]""", text)
	if p != None:
		punc_marks = len(p.groups())
	else:
		punc_marks = 0;

	v = []
	v += [len(text)*1.0/10, 0, words, punc_marks] #TODO: replace zero with number of lines
	words = text.split(" ")
	maxlen = 0
	for word in words:
		if len(word) > maxlen:
			maxlen = len(word)
	v += [maxlen]
	return v

def emojiAnalysis(text, detailed = True):
	#No of real emoji
	#No of ascii emoji
	#(detailed) No of each individual emoji
	v = [0,0]
	vd = []
	for emo in EMOJI:
		c = text.count(emo)
		v[0] += c
		vd.append(c)
	for emo in ASCII_EMOJI:
		c = text.count(emo)
		v[1] += c
		vd.append(c)
	if detailed:
		v += vd
	return v


def correctness(text):
	return []

def hebrewFeatures(text):
	return []

def contentAnalysis(text):
	s = [
	"חח","חחח","חחחח",
	"אני","אתה","אנחנו","הוא","היא","הם","הן",
	"אם","עם","נכון","כן","לא",
	"כאילו","אבל","וגם",
	]

	v = [0]*len(s)

	for i in range(len(s)):
		if text.find(s[i]) >= 0:
			v[i] = 1

	return v

def create_feature_vector(text):
	text = text.replace("@@",",")
	v = metadata(text)
	v += emojiAnalysis(text, False)
	v += contentAnalysis(text)
	v += correctness(text)
	v += hebrewFeatures(text)
	return v

def add_polynomial_features(v, deg = 2):
	if deg < 2:
		return v

	lastdeg = v
	newdeg = []
	polyv = []
	for d in range(1,deg):
		for unit in v:
			for subset in lastdeg:
				newdeg.append(unit*subset)
		polyv += lastdeg
		lastdeg = newdeg
	polyv += lastdeg
	return polyv

def add_quadratic_features(v):
	copy = v[:]
	for f1 in copy:
		for f2 in copy:
			v.append(f1*f2)
	return v

def add_polynomial_features(v, deg=2):
	if deg == 1:
		return v
	prevdeg = add_polynomial_features(v,deg-1)
	vpoly = []
	for x in v:
		for y in prevdeg:
			vpoly.append(x*y)
	vpoly += prevdeg
	return vpoly

if __name__ == "__main__":
	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
	else:
		f = open("data.csv")

	data = f.readlines()

	for entry in data:
		entry = entry.split(",")
		v = create_feature_vector(entry[0])
		v = add_polynomial_features(v,1)
		print v
		#break
