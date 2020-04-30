"""
main script for train/search for a specific path and Play
to clean the dirt position
"""
import os
from Bot.board import Problem
from Bot.QBot import train_bot, Q_play
from Bot.SearchBot import SearchAlgo
import matplotlib.pyplot as plt


def main():
	HEIGHT, WIDTH = 8, 10
	root_dir = os.path.realpath(os.path.dirname(__file__))
	data_dir = os.path.join(root_dir, 'data')
	if not os.path.exists(data_dir):
		os.mkdir(data_dir)
	# define the board problem
	p = Problem(height=HEIGHT, width=WIDTH)
	# define the search algo with BFS algorithm and play
	bfs_agent  = SearchAlgo(p, data_dir, algo='BFS')
	bfs_agent.play()
	# define the search algo with DFS algorithm and play
	dfs_agent  = SearchAlgo(p, data_dir, algo='DFS')
	dfs_agent.play()
	# define the search algo with UCS algorithm and play
	ucs_agent  = SearchAlgo(p, data_dir, algo='UCS')
	ucs_agent.play()

	# Train the Q-learning algorithm for the board problem
	# and save the reward figure during training
	Q, r = train_bot(data_dir, height=HEIGHT, width=WIDTH)
	plt.plot(r)
	plt.xlabel('Episode', fontsize=18)
	plt.ylabel('Total reward', fontsize=16)
	current_dir = os.path.realpath(os.path.dirname(__file__))
	plt.savefig(os.path.join(current_dir, 'data/Qdata/rewardsFig.png'))
	# play for a given board problem
	Q_play(Q, p, data_dir)


if __name__ == '__main__':
	main()