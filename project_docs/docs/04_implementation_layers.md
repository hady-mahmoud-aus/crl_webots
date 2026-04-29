# 04 — Implementation Layers

## Rule

Do not move to the next layer until the current layer runs and produces logs.

Claude Code can accelerate implementation, but it should not expand scope before the baseline pipeline works.

---

## Layer 0 — Environment smoke test

Goal: prove Webots control works.

Implement:

- e-puck sensor reading
- motor commands
- GPS/InertialUnit access
- reset logic
- fixed target
- proximity-based collision detection
- scripted forward/rotate actions
- simple target distance and bearing computation for logging

Success criterion:

- robot can execute scripted actions and log observations, search rewards, target distance, and collision flags.

---

## Layer 1 — Minimal search environment with deterministic homing

Goal: create a valid RL search loop and post-reveal homing routine.

Implement:

- fixed search observation vector
- 3 RL actions: `forward`, `rotate_left`, `rotate_right`
- GPS-based visited-cell tracking
- target reveal logic
- additive search reward with reveal bonus
- target reveal as RL success
- deterministic homing after reveal
- simple homing collision recovery
- episode metrics separating search and homing

Success criterion:

- random policy produces valid search transitions and metrics.
- when the target is revealed, RL control stops and deterministic homing runs to completion or timeout.

---

## Layer 2 — Double DQN search baseline`

Goal: train a working search policy in one scene.

Implement:

- custom PyTorch Q-network
- target Q-network
- replay buffer for search transitions only
- Double DQN update using `done_search`
- epsilon-greedy exploration
- checkpointing
- metrics logging
- deterministic homing called only after reveal, outside the replay buffer

Success criterion:

- policy improves on $T_1$ compared with random using target reveal rate, decision steps to reveal, coverage, or search return.

---

## Layer 3 — Sequential fine-tuning baseline

Goal: establish the continual-learning problem for search.

Train:

1. train on $T_1$, evaluate on $T_1$
2. train on $T_2$, evaluate on $T_1,T_2$
3. train on $T_3$, evaluate on $T_1,T_2,T_3$

Use target reveal rate as the main old-scene performance score.

Success criterion:

- sequential training runs end-to-end and old-scene target reveal performance is logged.

---

## Layer 4 — Selective episodic replay

Goal: add the simplest continual-learning mechanism.

Implement:

- top-$K$ search episode selection per scene
- episode ranking based primarily on target reveal success
- old search episode storage
- mixed replay batches
- replay-only experiment variant

Success criterion:

- replay variant runs and can be compared against fine-tuning using reveal rate and forgetting.

---

## Layer 5 — EWC-style regularization

Goal: add parameter-level retention for the search policy.

Implement:

- parameter snapshot after each scene
- squared-gradient importance estimate from DQN search loss
- online EWC accumulator
- EWC loss during later scenes
- EWC and replay+EWC variants

Success criterion:

- variants run without numerical instability and produce comparable search metrics.

---

## Layer 6 — Optional extensions

Only add after Layers 0–5 work.

Possible extensions:

- 5-action macro-action set with diagonals
- moving obstacles
- spawn randomization
- target randomization
- improved deterministic homing recovery
- homing diagnostic videos
- longer training runs
- video/demo recording
- hyperparameter sweeps

Do not add learned homing unless the simplified search-only continual RL system already works and the project timeline allows a clearly separated extension.

## Recommended cutoff if time is short

If the deadline is close, stop at:

> Layer 4: Double DQN search + sequential evaluation + selective replay + deterministic post-reveal homing.

This is already a defensible project if the experiments and plots clearly show target reveal performance and forgetting across scenes.
