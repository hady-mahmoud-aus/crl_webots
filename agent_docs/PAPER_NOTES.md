# PAPER_NOTES.md

## Purpose

Short implementation-relevant paper notes.

Full paper notes remain in `papers/`.

## KGCRL

Relevant inspiration:

- sequential multiscene navigation,
- catastrophic forgetting,
- EWC-style parameter retention,
- forgetting evaluation.

This project does not implement KGCRL exactly because it does not use DDPG, continuous velocity actions, A*/PID knowledge guidance, or KGCRL's exact actor Fisher.

Safe wording:

> KGCRL motivates EWC-style regularization for incremental navigation, but this project adapts the idea to a discrete Double DQN macro-action controller.

## OPR

Relevant inspiration:

- storing high-quality previous episodes,
- replaying selected past experience,
- reducing forgetting with small memory.

This project does not implement OPR exactly because it does not use A3C/ACER, stored policy probabilities, or visual target-incremental navigation.

Safe wording:

> OPR motivates selective storage of high-quality episodes, but this project implements a simpler DQN-compatible selective replay buffer.
