# Continual RL Webots e-puck Project Docs

This folder contains the current project documentation set for the Webots continual reinforcement learning project, aligned with the current codebase.

## Project summary

The project trains an e-puck or similar robot in Webots on sequential navigation scenes:

1. `T1`: empty room
2. `T2`: static obstacles
3. `T3`: moving obstacles, or a harder obstacle scene if dynamic obstacles are unstable

The current code implements a **single Double DQN controller** with two behavior regimes:

1. **Pre-reveal search:** the target is hidden from the policy. The observation contains local visited-cell flags, dwell/loop indicators, proximity sensors, heading features, and zeroed target-relative features. The policy explores, avoids revisits/stalls/collisions, and tries to enter the target reveal radius.
2. **Post-reveal learned approach:** once the target is revealed, the same DQN policy continues acting with target distance and bearing now included in the observation. The reward switches to a target-approach reward until the target is reached or the episode times out.

The continual RL problem is therefore **scene-incremental target-revealing navigation with learned post-reveal approach**, not a separate non-learned controller setup.

## Current method statement

> **Custom PyTorch Double DQN for target-revealing Webots navigation, with pre-reveal search rewards, post-reveal target-approach rewards, OPR-inspired Selective Search Episode Replay (SSER), and EWC-style Q-network regularization inspired by KGCRL.**

This is an inspired-by adaptation. It should not be described as an exact implementation of OPR or KGCRL.

## Source-of-truth choices

Use these defaults unless a later experiment explicitly changes them:

- RL algorithm: custom PyTorch Double DQN
- RL control scope: both pre-reveal search and post-reveal target approach
- Initial action set: `forward`, `rotate_right`, `rotate_left` in code action-index order
- Policy observation: 19-D compact observation
- Cell size: `0.1 m`
- Network: MLP with two hidden layers of 256 units
- Replay: current replay buffer; SSER can mix old selected episode transitions into later-scene training
- SSER ratio: `75%` current replay and `25%` old SSER replay in replay-enabled minibatches
- Continual regularization: EWC-style Q-network regularizer using the current Q-output-sensitivity importance approximation
- Reward: pre-reveal search reward plus reveal bonus; post-reveal target-approach reward after reveal
- Main continual-learning metric: target reveal rate
- Auxiliary/final metric: target reach rate after reveal
- Experiment orchestration: root schedule scripts under `schedules/`
- Implementation priority: working pipeline before additional novelty

## Current implementation caveats

- SSER currently stores only episodes where the target is reached, even though target reveal is the main continual-learning metric.
- Current EWC importance is based on sensitivity of `max_a Q(s,a)`, not squared gradients of the Double-DQN TD loss.
- Root schedule defaults are smoke-test values (`TRAIN_EPISODES = 2`, `EVAL_EPISODES = 1`) and should be increased for report-quality experiments.

## Document map

| File | Purpose |
|---|---|
| `00_project_scope_and_decisions.md` | Scope, current implementation assumptions, supported CRL variants, and known implementation gaps |
| `01_task_formulation.md` | Formal task definition, observations, rewards, success, and termination |
| `02_webots_environment_interface.md` | Webots/e-puck devices, actions, grid tracking, collision handling, controller inputs, and log fields |
| `03_method_math.md` | Implemented Double DQN, SSER, EWC-style regularization, current math, and caveats |
| `04_implementation_layers.md` | Layered build plan from baseline control to continual-learning variants |
| `05_training_and_evaluation.md` | Sequential training protocol, root schedule scripts, artifact dependencies, metrics, and outputs |
| `06_paper_alignment.md` | Safe alignment wording for OPR, KGCRL, and this adapted project |
