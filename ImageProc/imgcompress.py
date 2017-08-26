import sys
from PIL import Image
import numpy as np
#from sklearn.decomposition import PCA

im = Image.open(sys.argv[1]).convert("RGB")
chans = im.split()
K = int(sys.argv[2])

res = []
for chan in chans:
	px = np.array(chan, dtype=float)

	#normalize the mean
	n = px.shape[1]
	means = []
	for i in range(px.shape[0]):
		m = np.mean(px[i,])
		px[i,] -= m*np.ones((n,))
		means.append(m)

	cov = (1/(1.0*m))*np.matmul(px.T,px)

	U,S,V = np.linalg.svd(cov)

	Ured = U[:,0:K]

	Uapprox = np.matmul(Ured,Ured.T)


	pxres = np.matmul(px,Uapprox)

	for i in range(pxres.shape[0]):
		pxres[i,] += means[i]*np.ones((n,))
	res += [Image.fromarray(pxres).convert('L')]
resim = Image.merge('RGB',res)
resim.show()
