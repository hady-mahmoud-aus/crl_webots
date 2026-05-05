# 06 — Paper Alignment and Safe Claims

## Safe framing

This project is an inspired-by adaptation.

Use:

> Double DQN for discrete Webots target-revealing navigation, OPR-inspired Selective Search Episode Replay (SSER), and EWC-style Q-network regularization inspired by KGCRL.

Avoid:

> This project implements KGCRL and OPR.

Also avoid:

> This project exactly reproduces target-incremental visual navigation.

The project uses compact e-puck sensors in Webots, not egocentric RGB visual navigation.

## Alignment with OPR

OPR motivates:

- storing high-quality previous navigation experience,
- replaying selected past episodes,
- reducing catastrophic forgetting with small memory,
- retaining performance on learned targets/tasks while learning new ones.

This project does not implement original OPR because it does not use:

- A3C on-policy learning,
- ACER off-policy learning,
- Retrace targets,
- stored policy probabilities $\pi_t$,
- stored value/Q outputs from the behavior policy,
- target-incremental RGB visual navigation,
- `Done` action success in AI2-THOR.

Safe wording:

> OPR motivates the selective storage of high-quality navigation episodes. This project adapts that idea into Selective Search Episode Replay (SSER), a DQN-compatible replay mechanism that stores top-K high-quality previous-scene episodes and samples them during later-scene Double DQN training.

## SSER claim

Use:

> Selective Search Episode Replay (SSER) is an OPR-inspired replay mechanism for continual target-revealing navigation. The current code stores top-K reached episodes using a search-efficiency score based on coverage, collisions, and decision steps. During later-scene training, 25% of each replay-enabled Double DQN minibatch is sampled from this selective memory, allowing the agent to rehearse previous-scene behavior while learning the current scene.

Avoid:

> SSER is the same as OPR.

## Alignment with KGCRL

KGCRL motivates:

- sequential multiscene navigation,
- catastrophic-forgetting concern,
- EWC-style parameter retention,
- evaluation of forgetting across learned scenes.

This project does not implement:

- DDPG,
- continuous velocity actions,
- knowledge-guided A*/PID exploration,
- KGCRL's exact actor Fisher derivation,
- no-replay constraint.

Safe wording:

> KGCRL motivates the use of EWC-style regularization for incremental navigation, but this project adapts the idea to a discrete Double DQN controller using a Q-output-sensitivity diagonal importance approximation.

## Novelty claim

Use a modest novelty claim:

> This project adapts continual reinforcement learning to a target-revealing Webots navigation task and studies a lightweight hybrid of Double DQN, OPR-inspired selective episode replay, and EWC-style Q-network parameter retention across sequential scenes.

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

- “evaluates forgetting,”
- “attempts to reduce forgetting,”
- “provides a lightweight continual RL baseline,”
- “shows partial retention under SSER/EWC.”

## Clear problem statement for reports

Use this framing:

> The continual RL problem is formulated as sequential target-revealing navigation across Webots scenes. The learned Double DQN policy controls the robot throughout the episode. Before target reveal, target-relative features are hidden and the reward encourages coverage-oriented search. After reveal, target distance and bearing are enabled and the reward encourages reaching the target. The main continual-learning metric is target reveal rate, while target reach rate is reported as a final episode-success metric.
