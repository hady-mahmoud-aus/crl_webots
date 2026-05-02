import torch, random, math, collections
from torch import nn

from .buffer import ReplayBuffer
from .architecture import DQN

BATCH_SIZE = 64
GAMMA = 0.99 # discount factor
TAU = 0.005 # update rate
LR = 3e-4

# epsilon-greedy hyperparameter
EPS_START = 0.9
EPS_END = 0.01
EPS_DECAY = 2500

n_observations = 14
n_actions = 3
action_space = [0, 1, 2]

Transition = collections.namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))

class DQnManager:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.policy_net = DQN(n_observations, n_actions).to(self.device)
        self.target_net = DQN(n_observations, n_actions).to(self.device)
        self.target_net.load_state_dict(self.policy_net.state_dict())

        self.optimizer = torch.optim.AdamW(self.policy_net.parameters(), lr=LR, amsgrad=True)
        self.loss_fn = nn.SmoothL1Loss()

        self.steps_done = 0
        
    def getAction(self, state):
        sample = random.random()
        
        state = state.to(self.device)

        eps = EPS_END + (EPS_START - EPS_END) * math.exp(-self.steps_done / EPS_DECAY)
        self.steps_done += 1

        if sample > eps:
            with torch.no_grad():
                return self.policy_net(state).argmax(dim=1).item()

        return random.randint(0, 2)


    def optimizeModel(self, buffer):
        # Sample a random minibatch from replay memory
        transitions = buffer.sample(BATCH_SIZE)
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