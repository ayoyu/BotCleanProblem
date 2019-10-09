import random
import numpy as np
import math

def get_random_pos():
	return random.randint(0, 4), random.randint(0, 4)


def print_board(board):
	out = ''
	for y in board:
		row = ''.join(y)
		out += row + '\n'
	return out


def generate_random_board():
	board = np.array([['-'] * 5] * 5)
	y_b = y_d = x_b = x_d = 0
	while y_b == y_d and x_b == x_d:
		y_b, x_b = get_random_pos()
		y_d, x_d = get_random_pos()
	
	board[y_b][x_b], board[y_d][x_d] = 'b', 'd'
	return board


def generate_board(bot_pos, dirty_pos):
	board = np.array([['-'] * 5] * 5)
	board[bot_pos[0]][bot_pos[1]] = 'b'
	board[dirty_pos[0]][dirty_pos[1]] = 'd'
	return board


def get_distance(point1, point2):
	y = (point2[0] - point1[0]) ** 2
	x = (point2[1] - point1[1]) ** 2
	return math.sqrt(y + x)