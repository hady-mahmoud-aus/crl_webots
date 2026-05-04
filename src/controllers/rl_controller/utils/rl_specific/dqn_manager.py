import torch, random, math, collections
from torch import nn
from typing import Literal
from pathlib import Path

from .buffer import ReplayBuffer
from .architecture import DQN

BATCH_SIZE = 64
SELECTIVE_EPISODE_REPLAY_PERC = 0.25

GAMMA = 0.99 # discount factor
TAU = 0.005 # update rate
LR = 3e-4

# epsilon-greedy hyperparameter
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 2500

n_observations = 19
n_actions = 3
action_space = [0, 1, 2]

Transition = collections.namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

selective_replay_buffer = {'scene_1': [], 'scene_2': None} # each scene contains a list of K (10) episode buffers from evaluation

class DQnManager:
    def __init__(
        self, 
        policy: Literal['dqn', 'dqn_replay','dqn_ewc','dqn_replay_ewc'],
        scene_id: Literal[0, 1, 2],
        selective_replay_buffer: Path = None,
        model_params: Path = None, 
        eval = False
        ):
        
        self.eval = eval
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.loss_fn = nn.SmoothL1Loss()
        
        if model_params:
            self.fromSaved(model_params)
        else:
            self.policy_net = DQN(n_observations, n_actions).to(self.device)
            self.target_net = DQN(n_observations, n_actions).to(self.device)
            self.target_net.load_state_dict(self.policy_net.state_dict())
            
            self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=LR, amsgrad=True)
            
            self.steps_done = 0
        
        
        self.replay, self.ewc = getFlagsCRL(scene_id, policy)
        
        if self.replay:
            self.selective_replay_buffer = torch.load(selective_replay_buffer) # saved as .pt file

        if self.ewc:
            pass

    def getAction(self, state):
        state = state.to(self.device)
        
        if not self.eval:
            sample = random.random()

            eps = EPS_END + (EPS_START - EPS_END) * math.exp(-self.steps_done / EPS_DECAY)
            self.steps_done += 1

            if sample > eps:
                with torch.no_grad():
                    return self.policy_net(state).argmax(dim=1).item()

            return random.randint(0, 2)
        
        else: 
            with torch.no_grad():
                    return self.policy_net(state).argmax(dim=1).item()


    def optimizeModel(self, buffer: ReplayBuffer):
        
        # selective-replay handling
        if self.replay:
            batch_size_small = int(BATCH_SIZE * SELECTIVE_EPISODE_REPLAY_PERC)
            batch_size_large = BATCH_SIZE - batch_size_small
            
            transitions = self.sampleSelectiveReplay(batch_size_small) # scene-stratified sampling
            transitions += buffer.sample(batch_size_large)
            
            random.shuffle(transitions)
            
        # Sample a random minibatch from replay memory
        else: transitions = buffer.sample(BATCH_SIZE)
        
        
        batch = Transition(*zip(*transitions))

        # Convert stored states/actions/rewards into batched tensors
        state_batch = torch.stack(batch.state).to(self.device)  # [B, 14]
        action_batch = torch.tensor(batch.action, device=self.device).long().unsqueeze(1)
        reward_batch = torch.tensor(batch.reward, device=self.device).float()

        # Identify which transitions are non-terminal
        non_final_mask = torch.tensor(
            [s is not None for s in batch.next_state],
            device=self.device,
            dtype=torch.bool
        )

        non_final_next_states = torch.stack(
            [s for s in batch.next_state if s is not None]
        ).to(self.device)

        # Q-value predicted by the policy network for the action actually taken
        q_sa = self.policy_net(state_batch).gather(1, action_batch).squeeze(1)

        # Start with zero future value for terminal states
        next_values = torch.zeros(BATCH_SIZE, device=self.device)

        with torch.no_grad():
            # Double DQN:
            # policy_net chooses the best next action
            next_actions = self.policy_net(non_final_next_states).argmax(
                dim=1,
                keepdim=True
            )

            # target_net estimates the value of that chosen action
            next_values[non_final_mask] = self.target_net(non_final_next_states) \
                .gather(1, next_actions) \
                .squeeze(1)

        # Bellman target
        target = reward_batch + GAMMA * next_values

        # Train policy_net to match the target
        loss = self.loss_fn(q_sa, target)

        self.optimizer.zero_grad()
        loss.backward()

        # Prevent very large gradients
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)

        self.optimizer.step()


    def softUpdate(self):
        # Soft update of the target network's weights
        # θ′ ← τ θ + (1 −τ )θ′
        target_net_state_dict = self.target_net.state_dict()
        policy_net_state_dict = self.policy_net.state_dict()
        
        for key in policy_net_state_dict:
            target_net_state_dict[key] = policy_net_state_dict[key]*TAU + target_net_state_dict[key]*(1-TAU)
        self.target_net.load_state_dict(target_net_state_dict)
        
        
    def saveModel(self, path):
        torch.save({
            "policy_net": self.policy_net.state_dict(),
            "target_net": self.target_net.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "steps_done": self.steps_done,
        }, path)
        
    def fromSaved(self, path):
        checkpoint = torch.load(path, map_location=self.device)

        self.policy_net.load_state_dict(checkpoint["policy_net"])
        self.target_net.load_state_dict(checkpoint["target_net"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.steps_done = checkpoint["steps_done"]

        if self.eval:
            self.policy_net.eval()
            self.target_net.eval()
        else:
            self.policy_net.train()
            self.target_net.train()
            
    def sampleSelectiveReplay(self, batch_size):
        def flattenList(scene): return [transition for episode in scene for transition in episode]
        
        if self.selective_replay_buffer['scene_2'] is not None:
            half_batch = batch_size // 2
            
            scene_1 = flattenList(self.selective_replay_buffer['scene_1'])
            scene_2 = flattenList(self.selective_replay_buffer['scene_2'])
            
            transitions = random.sample(scene_1, half_batch)
            transitions += random.sample(scene_2, half_batch)
            
            return transitions
        
        else: 
            scene_1 = flattenList(self.selective_replay_buffer['scene_1'])
            return random.sample(scene_1, batch_size)
        
        
        
def getFlagsCRL(scene_id, policy): 
    """Returns -> (is_selective_replay, is_ewc)"""
    if scene_id == 2:
        return False, False
    else:
        replay = policy in ['dqn_replay' 'dqn_replay_ewc']
        ewc = policy in ['dqn_ewc','dqn_replay_ewc']
        
        return replay, ewc