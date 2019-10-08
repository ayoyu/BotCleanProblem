import random
from utils import (print_board, generate_random_board,
    get_distance, generate_board)
import numpy as np
import matplotlib.pyplot as plt


Possible_actions = {0: "UP", 1: "DOWN", 2: "LEFT", 3: "RIGHT"}
DISCOUNT = 0.99


def find_position(board, item):
    y = 0
    for row in board:
        if item in row:
            break
        else:
            y += 1
    x = board[min(4, y)].tolist().index(item)
    return y, x


def get_state(board):
    y_b, x_b = find_position(board, 'b')
    return y_b, x_b


# def get_reward(bot_pos, dirty_pos):
#     distance = get_distance(bot_pos, dirty_pos)
#     return - distance

def get_reward(bot_pos, dirty_pos):
    return -1 if bot_pos != dirty_pos else 10


def action_result(a, y_b, x_b):
    if a == "UP":
        y_b = max(0, y_b - 1) 
    elif a == "DOWN":
        y_b = min(4, y_b + 1)
    elif a == "LEFT":
        x_b = max(0, x_b - 1)
    elif a == "RIGHT":
        x_b = min(4, x_b + 1)
    return y_b, x_b

    
def env(board, a, dirty_pos):
    assert a in ["UP", "DOWN", "LEFT", "RIGHT"]
    y, x = find_position(board, "b")
    y_old, x_old = y, x
    y, x = action_result(a, y, x)
    board[y_old][x_old], board[y][x] = "-", "b"
    reward = get_reward((y, x), dirty_pos)
    done = True if (y, x) == dirty_pos else False
    return board, reward, done


def TrainBot():
    Q_table = np.random.uniform(low=0.0, high=2., size=(5, 5, 5, 5, 4))
    epsilon = 0.25
    alpha = 0.5
    rewards = []
    for step in range(1000):
        board = generate_random_board()
        dirty_pos = find_position(board, 'd')
        #state = get_state(board)
        total_reward = 0

        for i in range(10**4):
            
            state = get_state(board)
            y_b, x_b, y_d, x_d = (*state, *dirty_pos)
            if random.random() <= epsilon:
                a = np.random.choice(range(0, 4))
                
            else:
                
                a = np.argmax(Q_table[y_b][x_b][y_d][x_d])
            
            action_name = Possible_actions[a]
            next_board, r, done = env(board, action_name, dirty_pos)
            
            next_state = get_state(next_board)
            next_y_b, next_x_b = next_state
            Q_table[y_b][x_b][y_d][x_d][a] = Q_table[y_b][x_b][y_d][x_d][a] + alpha * (
                (r + DISCOUNT * max(Q_table[next_y_b][next_x_b][y_d][x_d])) -  Q_table[y_b][x_b][y_d][x_d][a])
            board = next_board
            total_reward += r
            rewards.append(total_reward)
            
            if done: break

        print('step :', step, '|total_reward: ', total_reward, '|done:', done
            , 'in: ', i)    
        epsilon *= 0.98
    return Q_table, rewards


def nextMove(Q):
    total_reward = 0
    board = generate_random_board()
    dirty_pos = find_position(board, 'd')
    print('Game Board')
    print_board(board)
    print('Play Game', '*' * 40)
    done = False
    step = 0
    while not done:
        state = get_state(board)
        y_b, x_b, y_d, x_d = (*state, *dirty_pos)
        a = np.argmax(Q[y_b][x_b][y_d][x_d])
        action_name = Possible_actions[a]
        next_board, reward, done = env(board, action_name, dirty_pos)
        board = next_board
        total_reward += reward
        step += 1
        print_board(next_board)
        print('step: ', step, '|reward:', reward, '|done:', done)
        print('*' * 50)
   
    print('total reward: ', total_reward)


if __name__ == '__main__':
    Q, r = TrainBot()
    plt.plot(r)
    plt.show()
    nextMove(Q)