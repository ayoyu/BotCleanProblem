import os
from Bot.CleanBot import TrainBot, nextMove
import matplotlib.pyplot as plt
import subprocess

if __name__ == '__main__':
	current_dir = os.path.realpath(os.path.dirname(__file__))
	Q, r = TrainBot()
	plt.plot(r)
	plt.xlabel('Episode', fontsize=18)
	plt.ylabel('Total reward', fontsize=16)
	plt.savefig(os.path.join(current_dir, 'data/rewardsFig.png'))
	nextMove(Q)