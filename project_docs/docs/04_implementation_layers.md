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
- GPS/Compass access
- reset logic
- fixed target
- collision detection

Success criterion:

- robot can execute scripted actions and log observations/rewards.

---

## Layer 1 — Minimal RL environment

Goal: create a valid RL loop.

Implement:

- fixed observation vector
- 3 actions: `forward`, `rotate_left`, `rotate_right`
- GPS-based visited-cell tracking
- target reveal logic
- additive search reward
- homing reward
- episode termination

Success criterion:

- random policy produces valid transitions and metrics.

---

## Layer 2 — Double DQN baseline

Goal: train a working policy in one scene.

Implement:

- custom PyTorch Q-network
- target Q-network
- replay buffer
- Double DQN update
- epsilon-greedy exploration
- checkpointing
- metrics logging

Success criterion:

- policy improves on $T_1$ compared with random.

---

## Layer 3 — Sequential fine-tuning baseline

Goal: establish the continual-learning problem.

Train:

1. train on $T_1$, evaluate on $T_1$
2. train on $T_2$, evaluate on $T_1,T_2$
3. train on $T_3$, evaluate on $T_1,T_2,T_3$

Success criterion:

- sequential training runs end-to-end and old-scene performance is logged.

---

## Layer 4 — Selective episodic replay

Goal: add the simplest continual-learning mechanism.

Implement:

- top-$K$ episode selection per scene
- old episode storage
- mixed replay batches
- replay-only experiment variant

Success criterion:

- replay variant runs and can be compared against fine-tuning.

---

## Layer 5 — EWC-style regularization

Goal: add parameter-level retention.

Implement:

- parameter snapshot after each scene
- squared-gradient importance estimate
- online EWC accumulator
- EWC loss during later scenes
- EWC and replay+EWC variants

Success criterion:

- variants run without numerical instability and produce comparable metrics.

---

## Layer 6 — Optional extensions

Only add after Layers 0–5 work.

Possible extensions:

- 5-action macro-action set with diagonals
- moving obstacles
- spawn randomization
- target randomization
- reactive collision recovery
- longer training runs
- video/demo recording
- hyperparameter sweeps

## Recommended cutoff if time is short

If the deadline is close, stop at:

> Layer 4: Double DQN + sequential evaluation + selective replay.

This is already a defensible project if the experiments and plots are clear.
