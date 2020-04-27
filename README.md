# BotClean Using (Qlearning, BFS, DFS, UCS)

**Solve the BotClean problem using Reiforcement learning and Search graph frameworks**

**Algorithms used**:
- Breadth First Search 
- Depth First Search
- Uniform Cost Search
- Q-learning (table version)

**Goal :** The Bot needs to make smarter moves to clean the dirty cell on a board with dimensions HEIGHT=8, WIDTH = 10

## install Dependencies:

[docker](https://docs.docker.com/install/)

### Create the Bot container:
```
$ docker build -t cleanbot .
```

### run the Bot container with volume:

```
$ docker run -d -v $PWD/bots_data:/app/data cleanbot
```

### Now check the performance of your Bots:

- To view the logs and figures of the 4 Bots, check the ```./bots_data``` directory, you will find 4 directories:
```
├── BFS_data
│   ├── play_logs.txt
│   └── search_log.txt
├── DFS_data
│   ├── play_logs.txt
│   └── search_log.txt
├── Qdata
│   ├── play_logs.txt
│   ├── rewardsFig.png
│   └── train_logs.txt
└── UCS_data
    ├── play_logs.txt
    └── search_log.txt

```
- **Example of BFS play_log.txt:**

![Clean Game](./figures/BFSGame.png)

- **Example of Q-learning rewardsFig.png:**

![Rewards](./figures/rewardsFig.png)

## TO DO:
- Build a command line interface (CLI), to chose between algorithms
  and change the board dimensions