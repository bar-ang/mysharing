from PIL import Image
import sys
import numpy as np
import string
from sklearn.neural_network import MLPClassifier
import os

neunet = MLPClassifier(hidden_layer_sizes=(10,10,))

def loadTrainingSet(folder="Training"):
	for c in string.ascii_lowercase:
		try:
			for file in os.listdir("./%s/%s" % (folder,c)):
				im = Image.open("./%s/%s/%s" % (folder,c,file))
				print "./%s/%s/%s" % (folder,c,file)
		except:
			os.mkdir("./%s/%s" % (folder,c))
    		 

X, y, X_test, y_test = loadTrainingSet()
neunet.fit(X,y)

