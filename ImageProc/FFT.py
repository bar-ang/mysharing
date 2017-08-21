from PIL import Image
import numpy as np

im = Image.open(sys.argv[1]).convert("L")
px = numpy.matrix(im.load())

dft = np.fft2(px)

dftim = Image.fromarray(dft)

dftim.show()


