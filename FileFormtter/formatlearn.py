from sklearn.svm import OneClassSVM
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors
import numpy as np
import sys
import os

rootdir = sys.argv[1]

examples = 700
size = 4000
test_perc = 0.4

c = 0
feats = np.zeros((examples, size)).astype(np.byte)
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        f = open(os.path.join(subdir, file),'rb')
        b = f.read()
        if len(b) <= size:
        	#print np.frombuffer(b, dtype=np.byte)
        	feats[c,0:len(b)] = np.frombuffer(b, dtype=np.byte)
        	c += 1
    	if c >= examples:
    		print "breaked"
    		break

pca = PCA(n_components=1000)
pca.fit(feats)

feats = pca.transform(feats)

t = int(examples*(1-test_perc))
train = feats[:t,:]
test = feats[t:,:]


#clf = NearestNeighbors()
clf = OneClassSVM(kernel = 'rbf', verbose=True)
clf.fit(train)

v = (clf.predict(train) + 1)/2
print float(np.sum(v))/len(v)



v = (clf.predict(test) + 1)/2
print float(np.sum(v))/len(v)