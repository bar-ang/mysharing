import numpy as np
from numpy.matlib import *
from sklearn.linear_model import LogisticRegression
import textAnalyzer
import sys
import random

def loadData(filepath, cv_frac = 0.2, test_frac = 0.2, polynomial_degree = 2):
	X_train = []
	X_cv = []
	X_test =[]

	y_train = []
	y_cv = []
	y_test =[]

	f = open(filepath,'r')

	data = f.readlines()
	random.shuffle(data)

	c = 0
	cv_count  = int(len(data)*cv_frac)
	test_count =  int(len(data)*test_frac)
	train_count =  len(data) - cv_count - test_count

	testSen = []
	for entry in data:
		entry = entry.split(",")
		if len(entry) < 2 or entry[1].strip() == "?":
			continue
		v,u = textAnalyzer.create_feature_vector(entry[0])
		v = textAnalyzer.add_polynomial_features(v,polynomial_degree)

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



	return X_train,y_train, X_cv,y_cv, X_test,y_test,u


def evaluateResults(lr, X_test, y_test):
	tests = X_test.shape[0]
	return lr.score(X_test,y_test)

THRESH = 0.5
POLY_DEG = 2
if __name__ == "__main__":
	if len(sys.argv) > 1:
		alldata = loadData(sys.argv[1],cv_frac = 0, test_frac = 0.4, polynomial_degree=POLY_DEG)
	else:
		alldata = loadData("data.csv", cv_frac = 0, test_frac = 0.4, polynomial_degree=POLY_DEG)
	X_train = alldata[0]
	X_cv = alldata[2]
	X_test = alldata[4]

	y_train = alldata[1]
	y_cv = alldata[3]
	y_test = alldata[5]

	u = alldata[6]

	lr = LogisticRegression(C=5.0)
	lr.fit(X_train,ravel(y_train))


	train_succ_precent = evaluateResults(lr, X_train, y_train)
	test_succ_precent = evaluateResults(lr, X_test, y_test)
	c = 0
	for f in np.nditer(lr.coef_):
		if round(f*100,2) > 0.5:
			print "%s: %s" % (u[c],round(f*100,2))
		c += 1
	sys.stdout.write("\n")
	print "training accuracy: %s%%." %round(train_succ_precent*100,3)
	print "testing  accuracy: %s%%." %round(test_succ_precent*100,3)