from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity, min_transitions):
        self.memory = deque([], maxlen=capacity)
        self.min_transitions = min_transitions

    def push(self, transition: dict):
        """Save a transition"""
        self.memory.append(transition)

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)