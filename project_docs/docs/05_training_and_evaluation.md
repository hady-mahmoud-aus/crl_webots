# 05 — Training and Evaluation

## Training protocol

For each method variant:

1. initialize model,
2. train sequentially on $T_1,T_2,T_3$,
3. after each training scene, evaluate on all scenes learned so far,
4. save model checkpoints,
5. save logs and metrics.

Sequential schedule:

| Stage | Train scene | Evaluate scenes |
|---|---|---|
| 1 | $T_1$ | $T_1$ |
| 2 | $T_2$ | $T_1,T_2$ |
| 3 | $T_3$ | $T_1,T_2,T_3$ |

## Method variants

Minimum variants:

1. `finetune`: Double DQN only
2. `replay`: Double DQN + selective episodic replay

Stronger variants:

3. `ewc`: Double DQN + online EWC approximation
4. `replay_ewc`: Double DQN + selective replay + online EWC

## Evaluation seeds

Use fixed evaluation seeds for each scene. This makes training-stage comparisons more reliable.

Training may use randomization if stable, but evaluation should be consistent.

## Primary metrics

Track:

- success rate
- average return
- coverage count
- offline coverage ratio
- collision count
- decision steps to completion
- target reveal rate
- target reach rate

## Forgetting metric

Use success rate as the main performance score $A_i$.

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

- $A_i(T_i)$: performance on scene $i$ immediately after learning scene $i$
- $A_i(T_k)$: performance on scene $i$ after learning scene $k$

Positive forgetting means old-scene performance degraded.

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
    replay/
      selective_memory.pkl
    notes.md
```

## Minimum plots

For the report/presentation, generate:

1. success rate by scene and training stage,
2. forgetting after $T_2$ and $T_3$,
3. coverage count or coverage ratio,
4. collision count,
5. training return curve.

## Practical acceptance criteria

A successful code deliverable should show:

- random policy logs are valid,
- Double DQN improves over random on at least $T_1$,
- sequential training runs across all scenes,
- replay or EWC variant runs without crashing,
- old-scene evaluation is reported after each scene.
