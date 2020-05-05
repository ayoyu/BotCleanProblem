"""
Command Line Interface for the BotClean application
"""
import os
import argparse
import textwrap
from Bot.board import Problem
from Bot.QBot import train_bot, Q_play
from Bot.SearchBot import SearchAlgo
import matplotlib.pyplot as plt


AGENTS = [
	'BFS',
	'DFS',
	'UCS',
	'Qlearning'
]
HEIGHT, WIDTH = 8, 10


def main(args):
	agent = args.agent
	height, width = args.height, args.width
	maze = args.maze
	if maze and agent == 'Qlearning':
		raise NotImplementedError("Not Implemented yet choose the graph search algorithms for this type of problem")
	root_dir = os.path.realpath(os.path.dirname(__file__))
	data_dir = os.path.join(root_dir, 'data')
	if not os.path.exists(data_dir):
		os.mkdir(data_dir)
	p = Problem(height, width, maze=maze)
	if agent == 'Qlearning':
		Q, r = train_bot(data_dir, height=height, width=width)
		plt.plot(r)
		plt.xlabel('Episode', fontsize=18)
		plt.ylabel('Total reward', fontsize=16)
		current_dir = os.path.realpath(os.path.dirname(__file__))
		plt.savefig(os.path.join(current_dir, 'data/Qdata/rewardsFig.png'))
		# play for a given board problem
		Q_play(Q, p, data_dir)
	else:
		agent = SearchAlgo(p, data_dir, algo=agent)
		agent.play()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog = "BotClean",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent("""\


██████╗  ██████╗ ████████╗     ██████╗██╗     ███████╗ █████╗ ███╗   ██╗    
██╔══██╗██╔═══██╗╚══██╔══╝    ██╔════╝██║     ██╔════╝██╔══██╗████╗  ██║    
██████╔╝██║   ██║   ██║       ██║     ██║     █████╗  ███████║██╔██╗ ██║    
██╔══██╗██║   ██║   ██║       ██║     ██║     ██╔══╝  ██╔══██║██║╚██╗██║    
██████╔╝╚██████╔╝   ██║       ╚██████╗███████╗███████╗██║  ██║██║ ╚████║    
╚═════╝  ╚═════╝    ╚═╝        ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    
                                                                            

Run simulations with differents algorithms and differents dimensions of the board/maze 
to test the performance of your agent.
List of algorithms to use:
	- BFS:       Breadth First Search
	- DFS:       Depth First Search
	- UCS:       Uniform Cost Search
	- Qlearning: Qlearning (table version)

Check your agent's logs/figures of performance in the ./data directory that will
be created after running a simulation. 
"""
			),
		epilog=textwrap.dedent("""\
			Example usage:
			--------------
			- Run the game with Breadth First Search agent in a board with dimensions
			  HEIGHT x WIDTH:

			  	$ python bot_clean.py -H 10 -W 15 -a BFS

			- Run the game with Breadth First Search agent in a random maze with dimensions
			  HEIGHT x WIDTH:

			  	$ python bot_clean.py -H 10 -W 15 -a BFS --maze

			- Run the game with Q-learning agent in a board with default dimensions (8 x 10):

				$ python bot_clean.py -a Qlearning

			- RUN the game with the default algorithm Uniform Cost Search in a random maze:

				$ python bot_clean.py -H 7 -W 20 --maze

			- RUN the game with the defaults args agent(UCS), board dimensions(8 x 10):

				$ python bot_clean.py
			"""

			)
		)
	parser.add_argument(
		'-H', '--height', type=int, default=HEIGHT,
		help="""\
		choose the height dimension for the board game (default 8).
		"""
		)
	parser.add_argument(
		'-W', '--width', type=int, default=WIDTH,
		help="""\
		choose the width dimension for the board game (default 10).
		"""
		)
	parser.add_argument(
		'-a', '--agent', type=str, default='UCS', choices=AGENTS,
		help="""\
		choose the agent to use for the simulation game 
		"""
		)
	parser.add_argument(
		'-m', '--maze', action='store_true',
		help="""\
		boolean argument to generate a random maze for the game
		"""
	)
	args = parser.parse_args()
	main(args)