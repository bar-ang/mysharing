
from PIL import Image
from PIL import ImageFilter
import numpy as np
import sys
from sklearn import cluster

im = Image.open(sys.argv[1])
px = im.convert("RGB")

X = []
pos = []

kmeans = cluster.KMeans(n_clusters=int(sys.argv[2]))

quantim = Image.new("RGB", im.size, "red")

n,m = im.size[0], im.size[1]
for i in range(n):
	for j in range(m):
		r,g,b = px.getpixel((i,j))
		X.append([r,g,b])
		pos.append([i,j])
X = np.matrix(X)

print "Data loaded"

kmeans.fit(X)

centers = kmeans.cluster_centers_
centers = centers.astype(int)

clus = kmeans.predict(X)


pxquant = quantim.load()



print "Learning done. Generating Image"

for i in range(len(pos)):
	center = centers[clus[i]]
	pxquant[pos[i][0],pos[i][1]] = tuple(center)

im.show()
quantim.show()