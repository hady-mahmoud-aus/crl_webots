# 06 — Paper Alignment and Safe Claims

## Safe framing

This project is an inspired-by adaptation.

Use:

> Double DQN for discrete Webots macro-action control, selective episodic replay inspired by OPR, and DQN-compatible EWC-style regularization inspired by KGCRL.

Avoid:

> This project implements KGCRL and OPR.

## Alignment with KGCRL

KGCRL motivates:

- sequential multiscene navigation,
- catastrophic-forgetting concern,
- EWC-style parameter retention,
- evaluation of forgetting across learned scenes.

This project does not implement:

- DDPG,
- continuous velocity action space,
- knowledge-guided A*/PID exploration,
- KGCRL's exact actor Fisher derivation,
- no-replay constraint.

Safe wording:

> KGCRL motivates the use of EWC-style regularization for incremental navigation, but this project adapts the idea to a discrete Double DQN macro-action controller.

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

> OPR motivates selective storage of high-quality episodes, but this project implements a simpler DQN-compatible selective replay buffer.

## Novelty claim

Use a modest novelty claim:

> This project adapts continual reinforcement learning to a two-phase search-and-homing robotics task in Webots and studies a lightweight hybrid of DQN-compatible EWC-style parameter retention and selective high-quality episodic replay across sequential scenes.

## What not to overclaim

Do not claim:

- exact KGCRL reproduction,
- exact OPR reproduction,
- state-of-the-art performance,
- full visual navigation,
- real-world transfer,
- guaranteed prevention of forgetting.

## Report language

Use “reduces forgetting” only if the metrics support it.

Otherwise use:

- “evaluates forgetting”
- “attempts to reduce forgetting”
- “provides a lightweight continual RL baseline”
- “shows partial retention under selective replay/EWC”
