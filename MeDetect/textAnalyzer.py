#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def create_feature_vector(text):
	text = text.replace("@@",",")
	s = ["!","!!","!!!","!1"
	"?","??","???",
	"\"",
	"חח","חחח","חחחח",
	".","..","...",
	",",":",";","~","$","%","'","/","^","&"
	"(",")",
	"[","]",
	":)",":(",":-)",":-(",";-)",";-(","=[","=]",
	":D",":S",":X",":O",
	"👍","😪","😅","🤣","😀","😅","🤔","😜","✨","🌚",
	"😅","😳","😶","🤔","🤣","😺","😗","😛",
	"😬","😂",
	"אני","אתה","אנחנו","הוא","היא","הם","הן",
	"אם","עם","נכון","כן","לא",
	"כאילו","אבל","וגם",
	]

	v = [0]*len(s)

	for i in range(len(s)):
		if text.find(s[i]) >= 0:
			v[i] = 1

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
		v = add_quadratic_features(v)
		break
