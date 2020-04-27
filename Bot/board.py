import random
import math


HEIGHT, WIDTH = 8, 10
Actions = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}


def get_random_pos():
	"""
	get 2 random positions in th board (HEIGHT, WIDTH)
	"""
	y , x = random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1)
	return y, x


def print_board(board):
	"""
	print out the board
	"""
	out = ''
	for y in board:
		row = ''.join(y)
		out += row + '\n'
	return out


def generate_random_board():
	"""
	generate random board
	"""
	board = [['-'] * WIDTH for _ in range(HEIGHT)]
	y_b = y_d = x_b = x_d = 0
	while y_b == y_d and x_b == x_d:
		y_b, x_b = get_random_pos()
		y_d, x_d = get_random_pos()
	
	board[y_b][x_b], board[y_d][x_d] = 'b', 'd'
	return board


def find_position(board, item):
	"""
	find the postion of dirty('d') or bot('b') in a given board
	"""
	if item not in ['d', 'b']:
		raise ValueError("searched item need to be bot tag or dirty tag")
	y = 0
	for row in board:
		if item in row:
			break
		else:
			y += 1
	x = board[y].index(item)
	return y, x


def action_result(a, y, x):
	"""
	get the position result on the board given an action
	"""
	if a not in Actions.values():
		raise ValueError("action a need to be in the Possible_actions dictionnary")
	if a == "UP":
		y = max(0, y - 1) 
	elif a == "DOWN":
		y = min(HEIGHT - 1, y + 1)
	elif a == "LEFT":
		x = max(0, x - 1)
	elif a == "RIGHT":
		x = min(WIDTH - 1, x + 1)
	return y, x


class Problem:
	"""
	wrapper for encoding the board
	"""

	def __init__(self):
		self.board =  generate_random_board()
		self.init_bot_pos = find_position(self.board, 'b')
		self.dirty_pos = find_position(self.board, 'd')


	def __repr__(self):
		board_str = print_board(self.board)
		return board_str


	def getSuccessors(self, pos):
		"""
		get successors for a specific position on the board
		with the possible actions
		"""
		forbidden_actions = list()
		y, x = pos
		if y == 0:
			forbidden_actions.append('UP')
		elif y == HEIGHT - 1:
			forbidden_actions.append('DOWN')
		if x == 0:
			forbidden_actions.append('LEFT')
		elif x == WIDTH - 1:
			forbidden_actions.append('RIGHT')
		possible_actions = [
			a for a in Actions.values() if a not in forbidden_actions
		]
		successors = [
			(a, action_result(a, y, x)) for a in possible_actions 
		]
		return successors


	def is_goal(self, pos):
		return self.dirty_pos == pos


	def distance_to_dirty(self, pos):
		y, x = pos
		y_d, x_d = self.dirty_pos
		dis = math.sqrt((y_d - y)**2 + (x_d - x)**2)
		return dis