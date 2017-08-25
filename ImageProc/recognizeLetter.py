from PIL import Image
import sys
import numpy as np
import string
from sklearn.neural_network import MPLClassifier

neunet = MPLClassifier(hidden_layer_sizes=(10,10,))

def loadTrainingSet(folder="Training"):
	pass

X, y, X_test, y_test = loadTrainingSet()
neunet.fit(X,y)

