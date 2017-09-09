import sys
import numpy as np

fname = "p096_sudoku.txt"
SIZE = 9

if len(sys.argv) > 1:
	fname = sys.argv[1]

f = open(fname,'r')

def load_boards():
	text = f.readlines()
	boards = []
	
	first = True
	for line in text:
		if "grid" in line.lower():
			if not first:
				boards.append(currmat)
			else:
				first = False
			currmat = np.zeros((SIZE,SIZE), dtype=int)
			row = 0
		else:
			rowdata = np.matrix([int(s) for s in line.strip()])
			currmat[row,:] = rowdata
			row += 1
	return boards

def check_double(vals): #is there any double values?
	for i in range(len(vals)):
		for j in range(i):
			if vals[i] == vals[j]:
				return True
	return False

def gather_row(board, row):
	vals = list(board[row,:])
	return vals

def gather_col(board, col):
	vals = list(board[:, col])
	return vals

def gather_square(board, i,j, size):
	sq = np.ndarray.tolist(board[i:(i+size), j:(j+size)].reshape((1,SIZE))[0])
	return sq

def check_solution(board,cut = 3):
	for i in range(SIZE):
		if check_double(gather_row(board,i)) or check_double(gather_col(board,i)):
			return False
	for i in range(cut):
		for j in range(cut):
			if check_double(gather_square(board,i*board//cut,j*board//cut, board//cut)):
				return False
	return True

boards = load_boards()
board = boards[0]

v = check_solution(board,0,0,3)
print v