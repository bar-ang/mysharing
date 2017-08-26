import sys
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA

im = Image.open(sys.argv[1]).convert("RGB")

px = np.array(im, dtype=float)



m,n,p = px.shape


feat = np.zeros((m*n,3))
ret = np.zeros((m,n), dtype=int)
means = np.zeros((m*n,))

c = 0
for i in range(m):
	for j in range(n):
		ret[i,j] = c
		feat[c,] = px[i,j]
		avg = np.mean(feat[ret[i,j],])
		feat[ret[i,j],] -= avg*np.ones((3,))
		means[ret[i,j]] = avg
		c += 1

feat = np.matrix(feat)


print "start PCA"

pca = PCA(n_components=2)
pca.fit(feat)
ifeat = pca.transform(feat)

out = np.zeros((m,n,3))
for i in range(m):
	for j in range(n):
		out[i,j] = [ifeat[ret[i,j]][0],ifeat[ret[i,j]][1],0]
		out[i,j] += means[ret[i,j]]*np.ones((3,))

out = Image.fromarray(np.uint8(out))

im.show()
out.show()