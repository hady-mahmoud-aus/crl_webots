# Title

- store max 10,000 transitions in transition buffer
- newest transitions push out oldest transitions
- use collections.deque with maxlen

- batch size 64 sampled (no duplicates) for buffer per training step

- training step occurs between every action in episode.
- start dqn update steps once buffer reaches 500 transitions
