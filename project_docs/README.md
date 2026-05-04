# Continual RL Webots e-puck Project Docs

This folder contains the current project documentation set for the Webots continual reinforcement learning project, aligned with the uploaded codebase.

## Project summary

The project trains an e-puck or similar robot in Webots on sequential navigation scenes:

1. `T1`: empty room
2. `T2`: static obstacles
3. `T3`: moving obstacles, or a harder static-obstacle scene if dynamic obstacles are unstable

The current code implements a **single Double DQN controller** with two behavior regimes:

1. **Pre-reveal search:** the target is hidden from the policy. The observation contains local visited-cell flags, dwell/loop indicators, proximity sensors, heading features, and zeroed target-relative features. The policy explores, avoids revisits/stalls/collisions, and tries to enter the target reveal radius.
2. **Post-reveal learned approach:** once the target is revealed, the same DQN policy continues acting with target distance and bearing now included in the observation. The reward switches to a target-approach reward until the target is reached or the episode times out.

The continual RL problem is therefore **scene-incremental target-revealing navigation with learned post-reveal approach**, not a separate non-learned controller setup.

## Current method statement

> **Custom PyTorch Double DQN for target-revealing Webots navigation, with pre-reveal search rewards, post-reveal target-approach rewards, and planned continual-learning extensions using OPR-inspired Selective Search Episode Replay (SSER) and DQN-compatible online EWC.**

## Source-of-truth choices

Use these defaults unless a later experiment explicitly changes them:

- RL algorithm: custom PyTorch Double DQN
- RL control scope: both pre-reveal search and post-reveal target approach
- Initial action set: `forward`, `rotate_right`, `rotate_left` in code action-index order
- Policy observation: 19-D compact observation
- Cell size: `0.1 m`
- Network: MLP with two hidden layers of 256 units
- Replay: current replay buffer; planned SSER adds top-K high-quality previous-scene episodes
- Continual regularization: planned online EWC approximation using squared DQN-loss gradients
- Reward: pre-reveal search reward plus reveal bonus; post-reveal target-approach reward after reveal
- Main continual-learning metric: target reveal rate
- Auxiliary/final metric: target reach rate after reveal
- Implementation priority: working pipeline before additional novelty

## Document map

| File | Purpose |
|---|---|
| `00_project_scope_and_decisions.md` | Scope, current implementation assumptions, and planned extensions |
| `01_task_formulation.md` | Formal task definition, observations, rewards, and termination |
| `02_webots_environment_interface.md` | Webots/e-puck devices, actions, grid tracking, collision handling, and controller structure |
| `03_method_math.md` | Double DQN, current replay, planned SSER, planned online EWC, and losses |
| `04_implementation_layers.md` | Layered build plan from current code to continual-learning variants |
| `05_training_and_evaluation.md` | Sequential training protocol, metrics, outputs, and evaluation rules |
| `06_paper_alignment.md` | Safe alignment wording for OPR, KGCRL, and this adapted project |
