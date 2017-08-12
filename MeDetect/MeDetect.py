#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import numpy.matlib
import scipy
import scipy.optimize
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
	for i in range(m):
		h = hypotesis(theta,X[i].T)
		if h > 0 and h < 1:
			J += y[i]*np.log(h) + (1-y[i])*np.log(1-h)
	J /= -m
	return J

def costFunctionGrad(X,y, theta,lambd):
	m = np.shape(X)[0]
	n = np.shape(X)[1]
	grad = np.matlib.zeros((n, 1))
	for i in range(m):
		h = hypotesis(theta,X[i].T)
		for j in range(n):
			grad[j,0] += (h-y[i])*X[i,j]/m
	return grad

def training(X,y,lambd, init_theta):
	return scipy.optimize.fmin_bfgs(costFunction,init_theta)

def gradientDecentTraining(X,y,a,lambd, init_theta, verbose = False):
	theta = init_theta
	total = 13
	for i in range(total):
		J = costFunction(X,y,theta,lambd)
		grad = costFunctionGrad(X,y,theta,lambd)
		theta -= a*grad
		if verbose:
			print "%s out of %s" %(i, total)

	return theta


THRESH = 0.5
GRADDECENT_ALPHA = 100
if __name__ == "__main__":
	X_train = []
	X_cv = []
	X_test =[]

	y_train = []
	y_cv = []
	y_test =[]

	if len(sys.argv) > 1:
		f = open(sys.argv[1],'r')
	else:
		f = open("data.csv")

	data = f.readlines()

	c = 0
	cv_count  = 0 #int(len(data)*0.2)
	test_count =  int(len(data)*0.4)
	train_count =  len(data) - cv_count - test_count

	testSen = []
	for entry in data:
		entry = entry.split(",")
		v = textAnalyzer.create_feature_vector(entry[0])
		v = textAnalyzer.add_quadratic_features(v)

		if c < train_count:
			X_train.append(v)
			y_train.append(int(entry[1]))
		elif c < train_count + cv_count:
			X_cv.append(v)
			y_cv.append(int(entry[1]))
		else:
			X_test.append(v)
			y_test.append(int(entry[1]))
			testSen.append(entry[0])
		c += 1

	X_train = np.matrix(X_train)
	y_train = np.matrix(y_train).T
	X_cv = np.matrix(X_cv)
	y_cv = np.matrix(y_cv).T
	X_test = np.matrix(X_test)
	y_test = np.matrix(y_test).T

	if len(sys.argv) <= 2:
		theta = np.matrix([0] * np.shape(X_train)[1], dtype=np.float_).T
		theta = training(X_train,y_train,0,theta)
	else:
		tfile = open(sys.argv[2],"r").read().split(",")[:-1]
		theta = []
		for val in tfile:
			theta.append(float(val))
		theta = np.matrix(theta, dtype=np.float_).T

	J_train, grad_train = costFunction(X_train,y_train,theta,0)		
	J_test, grad_test = costFunction(X_test,y_test,theta,0)		

	print "train cost: %s" % J_train[0,0]
	print "test cost: %s" % J_test[0,0]

	if len(sys.argv) <= 2:
		out = open("theta","w")
		for coord in theta:
			out.write("%s," % coord[0,0])

	#for text in open("willISay.txt",'r').readlines():
	#	text = text.rstrip()
	#	v = textAnalyzer.create_feature_vector(text)
	##	v = np.matrix(v).T
	##	h = hypotesis(theta, v)[0,0]
	#	if h >= THRESH:
	#		ans = "YES"
	#	else:
	#		ans = "NO"
	#	print "\" %s \" -- %s (%s)" % (text, ans, h*100)

	