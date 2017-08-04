#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def create_feature_vector(text):
	s = ["!","!!","!!!","?","??","???","\"","חח","חחח","חחחח",".","..","...",",","(",")","[","]",":)",":("]

	v = [0]*len(s)

	for i in range(len(s)):
		if text.find(s[i]) >= 0:
			v[i] = 1

	return v


if __name__ == "__main__":
	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
	else:
		f = open("meSaying.txt")

	texts = f.readlines()

	for text in texts:
		v = create_feature_vector(text)
		print v