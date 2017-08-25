#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import random

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
	return v,["length","lines","words","puncs"]

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


def contentAnalysis(text, s):
	v = [0]*len(s)
	u = []
	for i in range(len(s)):
		v[i] = text.count(s[i])
		u.append(s[i])

	return v,u

def hebrewFeatures(text):
	pride = ["שיוויון","בחירה","הכבוד","חופש","גאווה","דת"
	,"תורה","תועבה","סדום","עמורה","מחלה","סוטים","גאים",
	"אנשים","יפים","טובים","מקסים","מקסימים","שוטרים","מחליא",
	"צואה","נתניהו","תודה","מחמם","לב","ירושלים","חורבן","חרבה",
	"עיוות","מעוות","תמיד","חוק","מצעד","בהמות","כיפה","עדינים","טובי",
	"חסימת","חסימות","כבישים","אבדון","תמיכה","נורמלי","נורמלים","נורמליים",
	"ערומים","ערום","עירום","נמוך","בהמי","קומץ","תקשורת",
	"ביתמשפט","ביתהמשפט","השפלת","השפלה","נשים","נקבות","בנות",
	"אחים","אחיות","אחי","אחיי","רפואה","טינופת","חילול","שבת","גאווה","מגעילות"]
	return contentAnalysis(text,pride)

common = [
	"חח","חחח","חחחח",
	"אני","אתה","אנחנו","הוא","היא","הם","הן",
	"אם","עם","נכון","כן","לא",
	"כאילו","אבל","וגם",
	]


def create_feature_vector(text):
	text = text.replace("@@",",")
	v,u = metadata(text)
	#v += emojiAnalysis(text, False)
	#v += contentAnalysis(text)
	#v += correctness(text)
	v2,u2 = hebrewFeatures(text)
	v += v2
	u += u2
	return v,u


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

	data = random.suffle(f.readlines())

	for entry in data:

		entry = entry.split(",")
		v = create_feature_vector(entry[0])
		v = add_polynomial_features(v,2)
		print v
		#break
