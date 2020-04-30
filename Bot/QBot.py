import os
import random
from .board import (print_board, generate_random_board,
                    find_position, Actions, action_result)
import numpy as np
from copy import deepcopy


DISCOUNT = 0.99


def get_state(board):
    y_b, x_b = find_position(board, 'b')
    return y_b, x_b


def get_reward(bot_pos, dirty_pos):
    return -1 if bot_pos != dirty_pos else 10

    
def env(board, a, dirty_pos, height, width):
    if a not in Actions.values():
        raise ValueError("undefined action for this board problem")
    y_old, x_old = find_position(board, "b")
    y, x = action_result(a, y_old, x_old, height, width)
    board[y_old][x_old], board[y][x] = "-", "b"
    reward = get_reward((y, x), dirty_pos)
    done = True if (y, x) == dirty_pos else False
    return board, reward, done


def train_bot(data_dir, height, width):
    """
    Args:
    ------
        data_dir (str): path for logs data directory
    
    Returns:
    --------
        Q_table(numpy 5D)
        rewards: list of rewards
    """
    logs = ''
    # the state is encoded with Bot position et dirty position
    # Bot (5x_b, 5y_b) and Dirty (5x_d, 5y_d) Q_table[y_b][x_b][y_d][x_d]
    Q_table = np.random.uniform(low=0.0,
                                high=2.,
                                size=(height, width, height, width, 4)
                                )
    epsilon = 0.25
    alpha = 0.5
    rewards = []
    for step in range(10000):
        board = generate_random_board(height, width)
        dirty_pos = find_position(board, 'd')
        total_reward = 0

        for i in range(10**4):
            
            state = get_state(board)
            y_b, x_b, y_d, x_d = (*state, *dirty_pos)
            if random.random() <= epsilon:
                a = np.random.choice(range(0, 4))
            else:
                a = np.argmax(Q_table[y_b][x_b][y_d][x_d])
            
            action_name = Actions[a]
            next_board, r, done = env(board,
                                    action_name,
                                    dirty_pos,
                                    height,
                                    width
                                )
            next_state = get_state(next_board)
            next_y_b, next_x_b = next_state
            Q_table[y_b][x_b][y_d][x_d][a] = Q_table[y_b][x_b][y_d][x_d][a] + alpha * (
                (r + DISCOUNT * max(Q_table[next_y_b][next_x_b][y_d][x_d])) -  Q_table[y_b][x_b][y_d][x_d][a])
            board = next_board
            total_reward += r
        
            if done: break
        rewards.append(total_reward)
        logs += f"Episode: {step} |total_reward: {total_reward} |done: {done} |do it in : {i} step\n"   
        epsilon *= 0.98
    q_data_dir = os.path.join(data_dir, 'Qdata')
    if not os.path.exists(q_data_dir):
        os.mkdir(q_data_dir)
    with open(os.path.join(q_data_dir, 'train_logs.txt'), 'w') as file:
        file.write(logs)

    return Q_table, rewards


def Q_play(Q, Problem, data_dir):
    """
    Args:
    -----
        Q(numpy 5D): Q table resulting from the training
        Problem instance: the board problem to solve
        data_dir (str): path for logs data directory
    """
    total_reward = 0
    board = deepcopy(Problem.board)
    dirty_pos = Problem.dirty_pos
    game_board = str(Problem)
    height, width = Problem.height, Problem.width
    Play_logs = 'Game Board Q-learning\n' + game_board + 'Play Game' \
                + '*' * 40 + '\n'
    done = False
    step = 0
    while not done:
        state = get_state(board)
        y_b, x_b, y_d, x_d = (*state, *dirty_pos)
        a = np.argmax(Q[y_b][x_b][y_d][x_d])
        action_name = Actions[a]
        next_board, reward, done = env(board,
                                    action_name,
                                    dirty_pos,
                                    height,
                                    width
                                )
        board = next_board
        total_reward += reward
        step += 1
        next_game_board = print_board(next_board)
        meta_step = f'step: {step} |reward: {reward} |done: {done}\n' + '*' * 50
        step_log = next_game_board + meta_step + '\n'
        Play_logs += step_log
    Play_logs += f'Game total reward: {total_reward}'
    q_data_dir = os.path.join(data_dir, 'Qdata')
    if not os.path.exists(q_data_dir):
        os.mkdir(q_data_dir)
    with open(os.path.join(q_data_dir, 'play_logs.txt'), 'w') as file:
        file.write(Play_logs)