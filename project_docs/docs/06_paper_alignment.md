# 06 — Paper Alignment and Safe Claims

## Safe framing

This project is an inspired-by adaptation.

Use:

> Double DQN for discrete Webots search control, selective episodic replay inspired by OPR, and DQN-compatible EWC-style regularization inspired by KGCRL, with deterministic post-reveal homing.

Avoid:

> This project implements KGCRL and OPR.

Also avoid:

> The RL agent learns both search and homing.

The RL agent learns search/exploration until target reveal. Homing is handled by a fixed controller.

## Alignment with KGCRL

KGCRL motivates:

- sequential multiscene navigation,
- catastrophic-forgetting concern,
- EWC-style parameter retention,
- evaluation of forgetting across learned scenes.

This project does not implement:

- DDPG,
- continuous velocity action space,
- learned homing control,
- knowledge-guided A*/PID exploration,
- KGCRL's exact actor Fisher derivation,
- no-replay constraint.

Safe wording:

> KGCRL motivates the use of EWC-style regularization for incremental navigation, but this project adapts the idea to a discrete Double DQN search controller. The post-reveal homing behavior is deterministic and is not learned by the RL policy.

## Alignment with OPR

OPR motivates:

- storing high-quality previous experience,
- replaying selected past episodes,
- reducing catastrophic forgetting with small memory.

This project does not implement:

- A3C/ACER,
- stored policy probabilities,
- stored policy/value outputs for off-policy correction,
- target-incremental visual navigation,
- exact optimal policy replay.

Safe wording:

> OPR motivates selective storage of high-quality episodes, but this project implements a simpler DQN-compatible selective replay buffer for target-revealing search episodes.

## Novelty claim

Use a modest novelty claim:

> This project adapts continual reinforcement learning to a target-revealing search task in Webots and studies a lightweight hybrid of DQN-compatible EWC-style parameter retention and selective high-quality episodic replay across sequential scenes. A deterministic controller handles post-reveal homing, keeping the learned continual RL problem focused on search and exploration.

## What not to overclaim

Do not claim:

- exact KGCRL reproduction,
- exact OPR reproduction,
- state-of-the-art performance,
- full visual navigation,
- learned homing,
- real-world transfer,
- guaranteed prevention of forgetting.

## Report language

Use “reduces forgetting” only if the metrics support it.

Otherwise use:

- “evaluates forgetting”
- “attempts to reduce forgetting”
- “provides a lightweight continual RL baseline for target-revealing search”
- “shows partial retention under selective replay/EWC”

## Clear problem statement for reports

Use this framing:

> The continual RL problem is formulated as sequential target-revealing search across Webots scenes. The learned policy controls the robot only during search. When the target is revealed, control switches to a deterministic homing routine that turns toward the target and moves forward with simple collision recovery. Therefore, the main evaluation metric for continual RL is target reveal rate, while target reaching after reveal is logged as an auxiliary homing diagnostic.
