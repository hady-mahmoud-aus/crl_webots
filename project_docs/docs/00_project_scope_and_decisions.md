# 00 — Project Scope and Decisions

## Current goal

Build a working Webots e-puck continual reinforcement learning pipeline for sequential **target-revealing search**, followed by deterministic homing.

The implementation goal is not to reproduce KGCRL or OPR exactly. The project adapts their ideas into a simpler codebase:

> Double DQN for discrete search control, selective episodic replay for rehearsal, and online EWC-style regularization for parameter retention.

The original dual RL problem, where the same agent must both search and home to the target, is intentionally simplified. The RL policy is responsible for finding/revealing the target. Once the target is revealed, the RL policy stops acting and a fixed deterministic homing controller takes over.

## One-week implementation rule

Always prioritize a working pipeline over extra sophistication.

Do not add new complexity until the current layer works and produces logs/metrics.

## Required deliverable for code

The code should be able to:

1. run Webots episodes,
2. collect search-phase transitions,
3. train a Double DQN policy to reveal the target,
4. switch to deterministic homing after reveal,
5. train sequentially across scenes,
6. evaluate old and current scenes using target reveal rate,
7. save metrics and checkpoints,
8. optionally enable selective replay and EWC.

## Scope boundaries

### In scope

- Webots e-puck or similar differential-drive robot
- low-dimensional sensors, not camera input
- GPS used for environment-side bookkeeping
- three sequential scenes
- fixed RL action and observation spaces across scenes
- Double DQN for search/exploration
- target reveal as the RL success condition
- deterministic post-reveal homing controller
- simple homing collision recovery
- selective episodic replay
- DQN-compatible online EWC approximation
- sequential evaluation and forgetting metrics based primarily on reveal rate

### Out of scope for the first working version

- exact KGCRL implementation
- exact OPR implementation
- learned homing policy
- progress-based RL homing reward
- DDPG or continuous velocity actions
- A*/PID knowledge-guided exploration for the RL phase
- camera-based visual navigation
- full map input to the policy
- architecture expansion methods
- large hyperparameter sweeps

## Simplifying defaults

Use these unless there is a strong reason to change them:

- **RL phase:** search only; stop RL control once the target is revealed.
- **Homing phase:** deterministic controller turns toward the target and moves forward until reached or timeout.
- **Actions:** start with 3 RL actions: `forward`, `rotate_left`, `rotate_right`.
- **Network:** MLP with two hidden layers of 128 units.
- **Replay ratio after Layer 4:** 80% current replay, 20% old selective replay.
- **EWC:** online EWC approximation, not multi-anchor EWC.
- **Parameter importance:** squared gradients of the DQN TD loss.
- **Grid cell size:** start with `c = 0.2 m`.
- **Reward:** additive search reward plus target-reveal bonus.
- **Success:** target revealed, not target reached.
- **Main metric:** target reveal rate.
- **Target features:** not required in the RL policy observation; target distance and bearing are used by the deterministic homing controller after reveal.
- **Moving obstacles:** optional if static scenes and sequential training are stable.

## Project method statement

Use this statement in reports or code comments:

> The proposed method trains a discrete-action Double DQN controller for continual target-revealing search in Webots e-puck scenes. Once the hidden target is revealed, the learned policy stops and a deterministic homing controller turns toward the target and moves forward. To reduce forgetting during search, the method combines selective episodic replay inspired by OPR with a DQN-compatible online EWC approximation inspired by KGCRL. The method is intentionally lightweight and adapted for a short Webots implementation timeline.
