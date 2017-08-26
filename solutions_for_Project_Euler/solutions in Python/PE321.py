def lst_swap(lst,a,b):
	t = lst[a]
	lst[a] = lst[b]
	lst[b] = t


class CounterGame(object):
	"""docstring for CounterGame"""

	def __init__(self, n):
		self.board = [1]*n + [0] + [-1]*n
		self.n = n
		
	def __str__(self):
		string = ""
		for t in self.board:
			if t == 0:
				string += "_ "
			elif t > 0:
				string += "O "
			elif t < 0:
				string += "X "
		return string

	def move(self, loc):
		if loc + self.board[loc] < 0 or loc + self.board[loc] > 2*self.n+1:
			return False
		if self.board[loc] == 0:
			return False
		if self.board[loc + self.board[loc]] == 0:
			lst_swap(self.board,loc + self.board[loc], loc)
		elif self.board[loc + self.board[loc]] == -1*self.board[loc] and self.board[loc + 2*self.board[loc]] == 0:
			lst_swap(self.board,loc + 2*self.board[loc], loc)
		else:
			return False
		return True

	def move_copy(self, loc):
		if loc + self.board[loc] < 0 or loc + self.board[loc] >= 2*self.n+1:
			return None
		cg = CounterGame(self.n)
		cg.board = self.board[:]
		if cg.board[loc] == 0:
			return None
		if cg.board[loc + cg.board[loc]] == 0:
			lst_swap(cg.board,loc + cg.board[loc], loc)
		elif (loc + 2*cg.board[loc] >= 0 and loc + 2*cg.board[loc] < cg.n*2+1 
				and cg.board[loc + cg.board[loc]] == -1*cg.board[loc] 
				and cg.board[loc + 2*cg.board[loc]] == 0):
			lst_swap(cg.board,loc + 2*cg.board[loc], loc)
		else:
			return None
		return cg

	def check(self, loc):
		if loc + self.board[loc] < 0 or loc + self.board[loc] >= 2*self.n+1:
			return False
		if self.board[loc] == 0:
			return False
		if self.board[loc + self.board[loc]] == 0:
			return True
		elif (loc + 2*self.board[loc] >= 0 and loc + 2*self.board[loc] < self.n*2+1 
				and self.board[loc + self.board[loc]] == -1*self.board[loc] 
				and self.board[loc + 2*self.board[loc]] == 0):
			return True
		else:
			return False
		return True

	def is_win(self):
		winboard = board = [-1]*self.n + [0] + [1]*self.n
		return self.board == winboard

	def possible_moves(self):
		locs = []
		for i in range(self.n*2+1):
			if self.check(i):
				locs.append(i)
		return locs

	def warning(self, loc):
		return loc >= 2 and loc < self.n*2-1 and self.board[loc + 2*self.board[loc]] == self.board[loc]

def bruteForce(cg, movlst):
	if cg == None:
		return -1
	moves = cg.possible_moves()
	for move in moves:
		if cg.warning(move):
			continue
		x = bruteForce(cg.move_copy(move), movlst)
		if x >= 0:
			movlst.append(cg)
			return x + 1
	if cg.is_win():
		movlst.append(cg)
		return 0
	else:
		return -1

movlst = []

cg = CounterGame(3)

print bruteForce(cg, movlst)

for m in movlst:
	print str(m)