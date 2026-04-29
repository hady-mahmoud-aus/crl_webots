# 05 — Training and Evaluation

## Training protocol

For each method variant:

1. initialize model,
2. train the search policy sequentially on $T_1,T_2,T_3$,
3. after each training scene, evaluate on all scenes learned so far,
4. run deterministic homing after target reveal for episode completion and auxiliary logging,
5. save model checkpoints,
6. save logs and metrics.

Sequential schedule:

| Stage | Train scene | Evaluate scenes |
|---|---|---|
| 1 | $T_1$ | $T_1$ |
| 2 | $T_2$ | $T_1,T_2$ |
| 3 | $T_3$ | $T_1,T_2,T_3$ |

## Method variants

Minimum variants:

1. `finetune`: Double DQN search only
2. `replay`: Double DQN search + selective episodic replay

Stronger variants:

3. `ewc`: Double DQN search + online EWC approximation
4. `replay_ewc`: Double DQN search + selective replay + online EWC

Deterministic homing should be identical across all variants so that differences come from the learned search policy.

## Evaluation seeds

Use fixed evaluation seeds for each scene. This makes training-stage comparisons more reliable.

Training may use randomization if stable, but evaluation should be consistent.

## Primary metrics

Track these as primary RL search metrics:

- target reveal rate
- average search return
- coverage count
- offline coverage ratio
- search collision count
- decision steps to reveal
- timeout rate before reveal

Use target reveal rate as the main success rate.

## Auxiliary homing metrics

Track these separately from RL performance:

- target reach rate after deterministic homing
- homing timeout rate
- homing recovery count
- homing collision/recovery events
- homing duration

These metrics help debug the deterministic controller, but they should not replace target reveal rate as the main continual RL metric.

## Forgetting metric

Use target reveal rate as the main performance score $A_i$.

After learning scene $T_k$:

$$
F^{(k)}
=
\frac{1}{k-1}
\sum_{i=1}^{k-1}
\left(
A_i(T_i)-A_i(T_k)
\right)
$$

where:

- $A_i(T_i)$: target reveal rate on scene $i$ immediately after learning scene $i$
- $A_i(T_k)$: target reveal rate on scene $i$ after learning scene $k$

Positive forgetting means old-scene target reveal performance degraded.

## Suggested output files

Use a simple run directory:

```text
runs/
  run_YYYYMMDD_HHMMSS/
    config.yaml
    checkpoints/
      scene_1.pt
      scene_2.pt
      scene_3.pt
    metrics/
      train_log.csv
      eval_log.csv
      forgetting.csv
      homing_log.csv
    replay/
      selective_memory.pkl
    notes.md
```

## Minimum plots

For the report/presentation, generate:

1. target reveal rate by scene and training stage,
2. forgetting after $T_2$ and $T_3$ using reveal rate,
3. coverage count or coverage ratio,
4. search collision count,
5. training search return curve.

Optional diagnostic plots:

1. deterministic homing reach rate after reveal,
2. homing recovery count,
3. decision steps to reveal.

## Practical acceptance criteria

A successful code deliverable should show:

- random policy logs are valid,
- deterministic homing runs after reveal without needing RL actions,
- Double DQN improves over random on at least $T_1$ using target reveal rate or search efficiency,
- sequential training runs across all scenes,
- replay or EWC variant runs without crashing,
- old-scene target reveal evaluation is reported after each scene.
