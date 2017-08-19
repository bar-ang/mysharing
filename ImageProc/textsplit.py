from PIL import Image
from PIL import ImageFilter
from PIL import ImageDraw
import numpy as np
import sys
from sklearn import cluster



def get_col_costs(im,expand=1): #todo: carrently word only on gray scale pictures
	pxm = im.load()
	v = [0]*im.size[0]
	m, n = im.size
	for i in range(m-expand):
		for e in range(expand):
			avg = 0
			for j in range(n):
				fw = pxm[i+e,j]*1.0/256.0
				avg += fw/n
			for j in range(n):
				fw = pxm[i+e,j]*1.0/256.0
				v[i] += (fw-avg)**2
	return v

def compress(v, tolerance = 0):
	last = v[0]
	u = [(v[0],1)]
	for i in range(1,len(v)):
		if v[i] > tolerance:
			u.append((v[i],1))
		else:
			u[-1] = (u[-1][0],u[-1][1]+1)
		last = v[i]
	return u

def slice_cost(v, col_costs): #todo: carrently word only on gray scale pictures
	cost = 0
	for vi in v:
		cost += col_costs[vi]
	return cost

def locopt(v, tolerance=0.9):
	#derive
	opts = []
	for i in range(1,len(v)-1):
		#print v[i-1],v[i],v[i+1]
		if v[i] < tolerance*v[i-1] and v[i] < tolerance*v[i+1]:
			opts.append(i)
	return opts

def locopt_compressed(v, tolerance=0.9):
	opts = []
	pos = 0
	for i in range(1,len(v)-1):
		if v[i][0] < tolerance*v[i-1][0] and v[i][0] < tolerance*v[i+1][0]:
			opts.append(pos) # + v[i][1]//4)
		pos += v[i][1]
	return opts


def hslice(im, horiz):
	slices = []
	if 0 not in horiz:
		horiz.append(0)
	if im.size[1] not in horiz:
		horiz.append(im.size[1])

	horiz.sort()
	for i in range(len(horiz)-1):
		w = horiz[i+1]-horiz[i]
		newim = im.crop((0,horiz[i],im.size[0],horiz[i]+w))
		slices.append(newim)
	return slices

def vslice(im, vert):
	slices = []
	if 0 not in vert:
		vert.append(0)
	if im.size[0] not in vert:
		vert.append(im.size[0])

	vert.sort()
	for i in range(len(vert)-1):
		w = vert[i+1]-vert[i]
		newim = im.crop((vert[i],0,vert[i]+w,im.size[1]))
		slices.append(newim)
	return slices

def show_vslice(im,vert, color=(255,0,0)):
	im = im.convert('RGB')
	if 0 not in vert:
		vert.append(0)
	if im.size[0] not in vert:
		vert.append(im.size[0])

	vert.sort()
	draw = ImageDraw.Draw(im)

	for i in range(len(vert)-1):
		w = vert[i+1]-vert[i]
		draw.line([(vert[i],0),(vert[i],im.size[1])], fill=color)

	im.show()
	del draw

def show_redundant(im,cc, color=(0,0,255), thresh = 5):
	im = im.convert('RGB')
	
	draw = ImageDraw.Draw(im)

	for i in range(len(cc)):
		if cc[i] <= thresh:
			draw.line([(i,0),(i,im.size[1])], fill=color)		

	im.show()
	del draw

def vslice_by_blanks(im,cc, color=(0,0,255), thresh = 5):
	im = im.convert('RGB')
	v = []
	draw = ImageDraw.Draw(im)
	inters = []
	curr_inter=0
	isopen = False
	for i in range(len(cc)):
		if cc[i] > thresh and isopen:
			inters.append((curr_inter,i-1))
			isopen = False
		elif cc[i] <= thresh and not isopen:
				isopen = True
				curr_inter = i
	for inter in inters:
		v.append((inter[0]+inter[1])//2)
	return v

im = Image.open(sys.argv[1])

threshold = 128  
im = im.point(lambda p: p > threshold and 255)  

cc = get_col_costs(im,expand = 3)
#ccc = compress(cc, tolerance = 0)
#opts = locopt_compressed(ccc, tolerance = 1)

opts = vslice_by_blanks(im,cc)

#show_redundant(im,cc)
show_vslice(im,opts)
#print opts
