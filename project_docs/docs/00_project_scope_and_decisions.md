# 00 — Project Scope and Decisions

## Current goal

Build a working Webots e-puck continual reinforcement learning pipeline for sequential search-and-homing.

The implementation goal is not to reproduce KGCRL or OPR exactly. The project adapts their ideas into a simpler codebase:

> Double DQN for discrete robot control, selective episodic replay for rehearsal, and online EWC-style regularization for parameter retention.

## One-week implementation rule

Always prioritize a working pipeline over extra sophistication.

Do not add new complexity until the current layer works and produces logs/metrics.

## Required deliverable for code

The code should be able to:

1. run Webots episodes,
2. collect transitions,
3. train a Double DQN policy,
4. train sequentially across scenes,
5. evaluate old and current scenes,
6. save metrics and checkpoints,
7. optionally enable selective replay and EWC.

## Scope boundaries

### In scope

- Webots e-puck or similar differential-drive robot
- low-dimensional sensors, not camera input
- GPS used for environment-side bookkeeping
- three sequential scenes
- fixed action and observation spaces across scenes
- Double DQN
- selective episodic replay
- DQN-compatible online EWC approximation
- sequential evaluation and forgetting metrics

### Out of scope for the first working version

- exact KGCRL implementation
- exact OPR implementation
- DDPG or continuous velocity actions
- A*/PID knowledge-guided exploration
- camera-based visual navigation
- full map input to the policy
- architecture expansion methods
- large hyperparameter sweeps

## Simplifying defaults

Use these unless there is a strong reason to change them:

- **Actions:** start with 3 actions: `forward`, `rotate_left`, `rotate_right`.
- **Network:** MLP with two hidden layers of 128 units.
- **Replay ratio after Layer 4:** 80% current replay, 20% old selective replay.
- **EWC:** online EWC approximation, not multi-anchor EWC.
- **Parameter importance:** squared gradients of the DQN TD loss.
- **Grid cell size:** start with `c = 0.2 m`.
- **Reward:** additive reward terms.
- **Target features:** fixed-size observation vector; zero target features before reveal.
- **Moving obstacles:** optional if static scenes and sequential training are stable.

## Project method statement

Use this statement in reports or code comments:

> The proposed method trains a discrete-action Double DQN controller for Webots e-puck search-and-homing across sequential scenes. To reduce forgetting, it combines selective episodic replay inspired by OPR with a DQN-compatible online EWC approximation inspired by KGCRL. The method is intentionally lightweight and adapted for a short Webots implementation timeline.
