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
- target sampling
- proximity-based collision detection
- scripted forward/rotate actions
- target distance and bearing computation for logging

Success criterion:

- robot can execute scripted actions and log observations, rewards, target distance, and collision flags.

---

## Layer 1 — Minimal target-revealing navigation loop

Goal: create a valid DQN-controlled episode loop.

Implement:

- 19-D observation vector
- 3 RL actions: `forward`, `rotate_right`, `rotate_left`
- GPS-based visited-cell tracking
- blocked-cell tracking after collisions
- dwell feature
- recent-loop score
- target reveal logic
- post-reveal target distance and bearing features
- pre-reveal search reward
- post-reveal target-approach reward
- episode metrics: reveal, reach, coverage, reward, collisions, decision steps

Success criterion:

- random policy produces valid transitions and metrics.
- target features are zero before reveal and enabled after reveal.
- episodes end on target reach or maximum decision steps.

---

## Layer 2 — Double DQN baseline

Goal: train a working policy in one scene.

Implemented/current components:

- custom PyTorch Q-network
- target Q-network
- replay buffer
- Double DQN update
- Smooth L1 loss
- epsilon-greedy exploration
- soft target-network update
- checkpointing
- metrics logging

Success criterion:

- policy improves on $T_1$ compared with random using target reveal rate, target reach rate, coverage, or return.

---

## Layer 3 — Sequential fine-tuning baseline

Goal: establish the continual-learning problem.

Train:

1. train on $T_1$, evaluate on $T_1$,
2. train on $T_2$, evaluate on $T_1,T_2$,
3. train on $T_3$, evaluate on $T_1,T_2,T_3$.

Use target reveal rate as the main old-scene performance score. Also report target reach rate.

Success criterion:

- sequential training runs end-to-end and old-scene reveal/reach performance is logged.

---

## Layer 4 — SSER selective episodic replay

Goal: add the simplest continual-learning mechanism.

Implement:

- top-K episode selection per scene
- episode ranking based on reveal success, reach success, coverage, collisions, steps, and return
- old episode memory
- mixed replay batches
- replay-only experiment variant

Recommended first replay ratio:

```text
80% current replay, 20% old SSER replay
```

Success criterion:

- SSER variant runs and can be compared against fine-tuning using reveal rate, reach rate, and forgetting.

---

## Layer 5 — EWC-style regularization

Goal: add parameter-level retention.

Implement:

- parameter snapshot after each scene
- squared-gradient importance estimate from DQN loss
- online EWC accumulator
- EWC loss during later scenes
- EWC and SSER+EWC variants

Success criterion:

- variants run without numerical instability and produce comparable metrics.

---

## Layer 6 — Optional extensions

Only add after Layers 0–5 work.

Possible extensions:

- 5-action macro-action set with diagonal/arc movements
- moving obstacles
- spawn randomization
- target randomization beyond current random target sampling
- improved collision recovery
- videos/demo recording
- longer training runs
- hyperparameter sweeps
- clean Gym-style environment API
- separate pre-reveal and post-reveal timeout fields
- explicit transition phase labels for search vs approach

## Recommended cutoff if time is short

If the deadline is close, stop at:

> Layer 4: Double DQN + sequential evaluation + SSER selective replay.

This is already a defensible project if the experiments and plots clearly show reveal performance, reach performance, and forgetting across scenes.
