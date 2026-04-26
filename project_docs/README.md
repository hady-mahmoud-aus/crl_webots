# Continual RL Webots e-puck Project Docs

This folder is the cleaned project documentation set for the Webots continual reinforcement learning project.

## Project summary

The project trains an e-puck or similar robot in Webots on sequential navigation scenes:

1. `T1`: empty room
2. `T2`: static obstacles
3. `T3`: moving obstacles or a harder static-obstacle variant if time is limited

The robot solves a two-phase task:

1. **Search phase:** explore unseen grid cells and avoid repeated/stalled behavior.
2. **Homing phase:** once the hidden target is revealed locally, approach it using target-relative distance and bearing.

The method is intentionally lightweight:

> **Custom PyTorch Double DQN + selective episodic replay inspired by OPR + DQN-compatible online EWC approximation inspired by KGCRL.**

## Source-of-truth choices

Use these defaults unless a later experiment explicitly changes them:

- RL algorithm: custom PyTorch Double DQN
- Initial action set: `forward`, `rotate_left`, `rotate_right`
- Observation: fixed-size compact vector
- Replay: current replay buffer plus top-K past episodes
- Continual regularization: online EWC approximation using squared DQN-loss gradients
- Reward: additive search reward and progress-based homing reward
- Implementation priority: working pipeline before additional novelty

## Document map

| File | Purpose |
|---|---|
| `docs/00_project_scope_and_decisions.md` | Scope, simplifications, and implementation rules |
| `docs/01_task_formulation.md` | Formal task definition, observations, rewards, and termination |
| `docs/02_webots_environment_interface.md` | Webots/e-puck devices, actions, grid tracking, and collision handling |
| `docs/03_method_math.md` | Double DQN, selective replay, online EWC, and combined loss |
| `docs/04_implementation_layers.md` | Layered build plan from smoke test to optional extensions |
| `docs/05_training_and_evaluation.md` | Sequential training protocol, baselines, metrics, and outputs |
| `docs/06_paper_alignment.md` | Safe alignment wording for KGCRL and OPR |
| `docs/07_old_to_new_mapping.md` | How the previous markdown files were reorganized |

## Planning notes

The earlier `task_1_takeaways.md` and `task_2_takeaways.md` should remain separate planning notes. Their practical decisions have been integrated into this cleaned doc set.
