#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import numpy.matlib
import textAnalyzer
import sys

def sigmoid(z):
	return (1+np.exp(-z))**(-1)

def hypotesis(theta, x):
	dotprod = np.dot(theta.T, x)
	return sigmoid(dotprod)

def costFunction(X,y, theta,lambd):
	J = 0
	m = np.shape(X)[0]
	n = np.shape(X)[1]
	grad = np.matlib.zeros((n, 1))
	for i in range(m):
		h = hypotesis(theta,X[i].T)
		J += y[i]*np.log(h) + (1-y[i])*np.log(1-h)
		for j in range(n):
			grad[j,0] += (h-y[i])*X[i,j]/m
	J /= -m
	#print J
	return J, grad

def gradientDecentTraining(X,y,a,lambd, init_theta):
	theta = init_theta
	for i in range(150):
		J, grad = costFunction(X,y,theta,lambd)
		theta -= a*grad

	return theta


THRESH = 0.5
if __name__ == "__main__":
	goods = []
	bads = []

	for text in open("meSaying.txt",'r').readlines():
		goods.append(textAnalyzer.create_feature_vector(text))

	for text in open("notMeSaying.txt",'r').readlines():
		bads.append(textAnalyzer.create_feature_vector(text))

	X = np.matrix(goods + bads, dtype=np.float_)
	y = np.matrix([1]*len(goods) + [0]*len(bads),dtype=np.float_).T

	theta = np.matrix([0] * np.shape(X)[1], dtype=np.float_).T

	theta = gradientDecentTraining(X,y,25,0,theta)

	for text in open("willISay.txt",'r').readlines():
		text = text.rstrip()
		v = textAnalyzer.create_feature_vector(text)
		v = np.matrix(v).T
		h = hypotesis(theta, v)[0,0]
		if h >= THRESH:
			ans = "YES"
		else:
			ans = "NO"
		print "\" %s \" -- %s (%s)" % (text, ans, h*100)

	