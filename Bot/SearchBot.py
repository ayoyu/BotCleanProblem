import os
from .utils import Queue, Stack, PriorityQueue
from .board import print_board, find_position, action_result
import math
import time
from copy import deepcopy


class State:
	"""
	Encode the state defined by:
		- bot position
		- action that lead to this position
		- parent noeud
	"""

	def __init__(self, pos, action=None, parent=None):
		self.pos = pos
		self.action = action
		self.parent = parent


	def __repr__(self):
		return f'{type(self).__name__}({self.action}, {self.pos})'


	def __eq__(self, state):
		return self.pos == state.pos


	def __hash__(self):
		return hash(self.pos)


	def is_root(self):
		return self.parent is None


	def expand(self, successors, queue):
		for a, succ_pos in successors:
			s = State(pos=succ_pos,
					action=a,
					parent=self)
			queue.put(s)


class SearchAlgo:
	"""
	Use 3 search algorithm:
		- BFS: Breadth First Search
		- DFS: Depth First Search
		- UCS: Uniform Cost Search
	"""

	def __init__(self, Problem, data_dir, algo='BFS'):
		if algo not in ['BFS', 'DFS', 'UCS']:
			raise ValueError(f'algo {algo} not found')
		self.Problem = Problem
		self.data_dir = data_dir
		if algo == 'BFS':
			self.container = Queue()
		elif algo == 'DFS':
			self.container = Stack()
		elif algo == 'UCS':
			self.container = PriorityQueue(Problem.distance_to_dirty)
		self.algo = algo


	def get_actions_path(self):
		search_log = ''
		actions = list()
		state = State(pos=self.Problem.init_bot_pos)
		frontier = self.container
		explored_states = list()
		while True:
			successors = [
				s for s in self.Problem.getSuccessors(state.pos) if s[1] not in explored_states 
			]
			state.expand(successors, frontier)
			search_log += f'Expand the {state} with {len(successors)} successors\n'
			explored_states.append(state.pos)
			if not frontier.empty():
				state = frontier.get()
				search_log += f' -> Get the {state} from the frontier to expand\n'
			if self.Problem.is_goal(state.pos):
				search_log += f'Reach the goal state {state}\n'
				break
		while not state.is_root():
			actions.append(state.action)
			state = state.parent
		return actions[::-1], search_log


	def _env(self, board, action):
		y_old, x_old = find_position(board, "b")
		y, x = action_result(action, y_old, x_old)
		board[y_old][x_old], board[y][x] = "-", "b"
		return board


	def play(self):
		start_search = time.time()
		actions, search_log = self.get_actions_path()
		search_time  = round((time.time() - start_search), 2)
		algo_data_dir = os.path.join(self.data_dir, f'{self.algo}_data')
		if not os.path.exists(algo_data_dir):
			os.mkdir(algo_data_dir)
		with open(os.path.join(algo_data_dir, 'search_log.txt'), 'w') as file:
			file.write(search_log)
		# to initiate the same board with 'd' tag for different algo
		# with the same problem instance in the main entrypoint (main.py)
		board = deepcopy(self.Problem.board)
		game_board = str(self.Problem)
		Play_logs = f'Game Board Search {self.algo} Time: {search_time} s\n' \
					+ game_board + 'Play Game' + '*' * 40 + '\n'
		step = 1
		for a in actions:
			next_board = self._env(board, a)
			next_game_board = print_board(next_board)
			meta_step = f'step: {step} |action: {a}\n' + '*' * 50
			step_log = next_game_board + meta_step + '\n'
			Play_logs += step_log
			board = next_board
			step += 1
		
		with open(os.path.join(algo_data_dir, 'play_logs.txt'), 'w') as file:
			file.write(Play_logs)