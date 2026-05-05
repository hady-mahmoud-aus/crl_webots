# 00 - Project Scope and Decisions

## Current goal

Build a working Webots e-puck continual reinforcement learning pipeline for sequential **target-revealing navigation** across scenes.

The current code uses one discrete-action Double DQN controller. Before target reveal, the target is hidden from the policy and the agent learns coverage-oriented search. After target reveal, the same learned policy continues acting with target-relative features enabled and receives a target-approach reward until the target is reached or the episode times out.

The implementation goal is not to reproduce KGCRL or OPR exactly. The project adapts their ideas into a simpler codebase:

> Double DQN for discrete Webots navigation, OPR-inspired Selective Search Episode Replay (SSER) for rehearsal, and EWC-style Q-network regularization for parameter retention.

## Implementation rule

Always prioritize a working pipeline over extra sophistication.

Do not add new complexity until the current layer works and produces logs/metrics.

## Required deliverable for code

The code should be able to:

1. run Webots episodes,
2. collect DQN transitions before and after target reveal,
3. train a Double DQN policy to reveal and then reach the target,
4. train sequentially across scenes,
5. evaluate old and current scenes using target reveal rate and target reach rate,
6. save logs, metrics, checkpoints, and enabled CRL artifacts,
7. optionally enable SSER/selective replay and EWC-style regularization.

## Scope boundaries

### In scope

- Webots e-puck or similar differential-drive robot
- low-dimensional sensors, not camera input
- GPS used for environment-side bookkeeping
- three sequential scenes
- fixed RL action and observation spaces across scenes
- Double DQN for discrete navigation control
- hidden target during pre-reveal search
- target distance and bearing exposed only after reveal
- target reveal as the primary continual-learning success condition
- target reaching as a final/auxiliary success condition
- proximity-based collision detection
- blocked-cell marking after forward collisions
- dwell and loop features for local anti-stall behavior
- recent-cell tracking
- SSER/selective episodic replay as the implemented OPR-inspired replay variant
- EWC-style Q-network regularization as the implemented KGCRL-inspired retention variant
- root schedule scripts under `schedules/` for sequential training and evaluation
- sequential evaluation and forgetting metrics based primarily on reveal rate

### Out of scope for the first working version

- exact KGCRL implementation
- exact OPR implementation
- A3C, ACER, Retrace, or OPR-style stored policy probabilities
- DDPG or continuous velocity actions
- A*/PID knowledge-guided exploration
- camera-based visual navigation
- full map input to the policy
- architecture expansion methods
- large hyperparameter sweeps

## Current implementation defaults

Use these unless there is a strong reason to change them:

- **RL phase before reveal:** target-hidden search.
- **RL phase after reveal:** same DQN policy continues with target distance and bearing enabled.
- **Actions:** 3 macro-actions: `forward`, `rotate_right`, `rotate_left`.
- **Network:** MLP with two hidden layers of 256 units.
- **Observation dimension:** 19.
- **Replay buffer:** capacity `10000`, warmup `500` transitions.
- **Batch size:** `64`.
- **Discount:** `gamma = 0.99`.
- **Soft target update:** `tau = 0.005`.
- **Optimizer:** AdamW, learning rate `3e-4`, AMSGrad enabled.
- **Exploration:** exponential epsilon decay from `0.9` to `0.01` with decay constant `2500`.
- **SSER old replay ratio:** `25%` old SSER transitions and `75%` current replay transitions in replay-enabled minibatches.
- **SSER memory:** top `K = 10` reached episodes per stored scene, ranked by current search-efficiency score.
- **EWC strength:** `lambda = 10.0`.
- **EWC importance:** current Q-output-sensitivity approximation, not yet TD-loss squared-gradient importance.
- **Grid cell size:** `0.1 m`.
- **Origin:** `(0, -0.9)`.
- **Reveal radius:** `0.35 m`.
- **Reach radius:** `0.15 m`.
- **Primary metric:** target reveal rate.
- **Final/auxiliary metric:** target reach rate.

## Current implementation gaps

These are current code-truth caveats, not intended final claims:

- SSER stores only episodes with `reached=True`, so reveal-only successes are not currently preserved despite reveal rate being the primary metric.
- The current EWC variant estimates parameter importance from sensitivity of `max_a Q(s,a)`, not from squared gradients of the Double-DQN TD loss.
- Saved SSER replay objects contain Python `Transition` instances; PyTorch artifact loading may require explicit non-weights-only loading support.
- Transitions do not store phase labels, scene ids, macro-action duration, or explicit done flags.

## Project method statement

Use this statement in reports or code comments:

> The proposed method trains a discrete-action Double DQN controller for continual target-revealing navigation in Webots e-puck scenes. The target is hidden during the search regime and revealed once the robot enters a reveal radius. After reveal, the same learned policy continues with target-relative distance and bearing features to reach the target. To evaluate forgetting across scenes, the code supports a fine-tuning baseline plus OPR-inspired Selective Search Episode Replay (SSER) and an EWC-style Q-network regularizer inspired by KGCRL. The method is intentionally lightweight and adapted for a short Webots implementation timeline; it should not be described as an exact KGCRL or OPR reproduction.
