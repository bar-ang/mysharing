from PIL import Image
import numpy as np
import sys

im = Image.open(sys.argv[1]).convert("L")
px = np.array(im, dtype=np.complexfloating)*(1/255.0)


out = np.fft.fft2(px)

print out

dftim1 = Image.fromarray(np.real(out)*(10.0))
dftim2 = Image.fromarray(np.imag(out)*(10.0))

dftim1.show()
dftim2.show()


