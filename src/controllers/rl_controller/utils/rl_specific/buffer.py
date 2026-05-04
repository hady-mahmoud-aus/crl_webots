from collections import deque
import random
import heapq


class ReplayBuffer:
    def __init__(self, capacity, min_transitions):
        self.memory = deque([], maxlen=capacity)
        self.min_transitions = min_transitions

    def push(self, transition):
        self.memory.append(transition)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# for selective episode replay
# stores top K episodes by metric score
class PriorityBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.heap = []
        self.counter = 0

    def push(self, score, item):
        entry = (score, self.counter, item)
        self.counter += 1

        if len(self.heap) < self.capacity:
            heapq.heappush(self.heap, entry)
        elif score > self.heap[0][0]:
            heapq.heapreplace(self.heap, entry)

    def items(self):
        return [item for _, _, item in sorted(self.heap, reverse=True)]

    def __len__(self):
        return len(self.heap)


# for EWC Fisher estimation
# when full, appends new transitions based on random probability
# all transitions are equally likely to be included
class ReservoirBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.n_seen = 0

    def push(self, transition):
        self.n_seen += 1

        if len(self.memory) < self.capacity:
            self.memory.append(transition)
            return

        i = random.randint(0, self.n_seen - 1)

        if i < self.capacity:
            self.memory[i] = transition

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)