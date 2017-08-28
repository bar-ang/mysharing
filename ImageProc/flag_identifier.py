import numpy as np
import sys
import os
from PIL import Image

#Unroll the image into a vector of size wXhX3
#Unroll the flag image into a vector of size wXhX3
#choose a comparing demention and use PCA to do the reduction

if len(sys.argv) < 2:
	print "please insert path to an image"
	sys.exit(0)

flags = {
	"russia" : 573,
	"cambodia" : 59,
	"cyprus" : 75,
	"denmark": 77,
	"macedonia": 8,
	"egypt": 83,
	"UK": 88,
	"bosnia": 86,
	"indonesia": 896,
	"finland": 91,
	"germany": 916,
	"france": 92,
	"the netherlands": 925,
	"lybia": 1265,
	"iran": 126,
	"korea": 121,
	"USA": 1214,
	#"the fire nation": 9901,
	#"bolton": 9902
	#"rose's battle flag": 9903
}

def unfold(matrix3d):
	m,n,d = matrix3d.shape
	v = np.zeros((m*n*d,))
	c = 0
	for i in range(m):
		for j in range(n):
			for k in range(d):
				v[c] = matrix3d[i,j,k]
				c += 1
	return v

def padding(v, dim):
	u =np.zeros((dim,))
	u[0:v.shape[0]] = v
	return u

def load_image(number, folder="flags", prefix="flag_",suffix=".gif"):
	im = Image.open("%s/%s%s%s" % (folder,prefix,str(number),suffix)).convert("RGB")
	px = np.array(im, dtype=float)/256
	return unfold(px)

def get_closest(v, U, k = 5):
	closest = {}
	worst = None
	for u in U.keys():
		d = np.linalg.norm(U[u]-v)
		if len(closest.keys()) < k:
			closest[u] = d
			if worst == None or d > closest[worst]:
				worst = u
		else:
			if d < closest[worst]:
				closest[u] = d
				del closest[worst]
				worst = min(closest, key=closest.get)
	return closest


inIm = Image.open(sys.argv[1]).convert("RGB")
inV = unfold(np.array(inIm, dtype=float)/256)

vector_flags = {}
dim = inV.shape[0]
for flag in flags.keys():
	vector_flags[flag] = load_image(flags[flag])
	if vector_flags[flag].shape[0] > dim:
		dim = vector_flags[flag].shape[0]

for flag in vector_flags.keys():
	vector_flags[flag] = padding(vector_flags[flag], dim)

inV = padding(inV, dim)


closest = get_closest(inV,vector_flags,1)

for k in closest:
	print k, closest[k]
