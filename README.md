# CleanBot-Qlearning Fun code :)

**Using Q_learning to solve the Clean-Bot problem**

**Goal :** The Bot needs to make smarter moves to clean the dirty cell.

## install Dependencies:

[docker](https://docs.docker.com/install/)

### Create Bot container:
```
$ docker build -t cleanbot .
```

### run the Clean Bot:

```
$ docker run -d -v bot_data:/app/data cleanbot
```

### Now check the performance of your Bot:

```
$ docker volume ls
```
 - **output**:
```
DRIVER              VOLUME NAME
local               bot_data
```
- To view the logs and figures of the Bot, CD to /var/lib/docker/volumes/bot_data, you will find 3 files:
```
Play_logs.txt  rewardsFig.png  train_logs.txt
```
- **Play_logs.txt:**

![Clean Game](./figures/CleanGame.png)

- **rewardsFig.png:**


![Rewards](./figures/rewardsFig.png)