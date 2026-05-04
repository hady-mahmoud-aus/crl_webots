# 05 — Training and Evaluation

## Training protocol

**TRAIN_EPISODES** = 2000

**EVAL_EPISODES** = 100

For each method variant:

1. initialize model,
2. train the policy sequentially on $T_1,T_2,T_3$,
3. after each training scene, evaluate on all scenes learned so far,
4. save model checkpoints,
5. save logs and metrics.

Sequential schedule:

| Stage | Train scene | Evaluate scenes |
|---|---|---|
| 1 | $T_1$ | $T_1$ |
| 2 | $T_2$ | $T_1,T_2$ |
| 3 | $T_3$ | $T_1,T_2,T_3$ |

## Current controller inputs

The top-level controller uses environment variables:

| Variable | Default | Purpose |
|---|---:|---|
| `SEED` | `42` | random seed |
| `NUM_EPISODES` | `2000` | number of episodes |
| `POLICY` | `dqn` | save-directory label |
| `SCENE_ID` | `0` | current scene id |
| `PARENT_SCENE` | `-1` | parent/previous scene label in filenames |
| `EVAL` | `False` | evaluation mode flag |
| `PARAMS_PATH` | `None` | checkpoint path |

## Method variants

Minimum variants:

1. `finetune`: Double DQN only
2. `replay`: Double DQN + SSER selective replay

Stronger variants:

3. `ewc`: Double DQN + online EWC approximation
4. `replay_ewc`: Double DQN + SSER selective replay + online EWC

All variants should use the same action space, observation structure, target sampling rules, and reward definitions unless the experiment explicitly states otherwise.

## Evaluation seeds

Use fixed evaluation seeds for each scene. This makes training-stage comparisons more reliable.

Training may use randomization if stable, but evaluation should be consistent.

## Primary metrics

Track these as primary RL navigation metrics:

- target reveal rate,
- target reach rate,
- average episode return,
- coverage count,
- collision count,
- decision steps,
- timeout rate.

Use **target reveal rate** as the main continual-learning score because reveal is the point where the hidden target is found. Use **target reach rate** as a final episode-success metric.

## Current per-episode log fields

The current logger records:

| Field | Description |
|---|---|
| `episode` | episode number |
| `scene_id` | scene id |
| `seed` | random seed |
| `revealed` | target entered reveal radius |
| `reached` | target entered reach radius |
| `timeout_before_reveal` | legacy timeout field |
| `unique_cells_covered` | visited-cell count |
| `reward` | total episode reward |
| `collisions` | collision count |
| `decision_steps` | number of DQN macro-actions |

Recommended future logging cleanup:

- split `timeout_before_reveal` into `timeout_before_reveal` and `timeout_after_reveal`,
- add `steps_to_reveal`,
- add `steps_after_reveal`,
- add `phase` labels to transitions.

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

- $A_i(T_i)$: target reveal rate on scene $i$ immediately after learning scene $i$,
- $A_i(T_k)$: target reveal rate on scene $i$ after learning scene $k$.

Positive forgetting means old-scene target reveal performance degraded.

Also compute the same metric with target reach rate as a secondary final-success analysis.

## Suggested output files

Use a simple run directory:

```text
runs/
  dqn/
    train-<parent>-<scene>-<episodes>-<seed>.csv
    train-<parent>-<scene>-<episodes>-<seed>.pt
  dqn_replay/
    ...
  dqn_ewc/
    ...
  dqn_replay_ewc/
    ...
```

A future more structured layout can be:

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
      sser_memory.pkl
    notes.md
```

## Minimum plots

For the report/presentation, generate:

1. target reveal rate by scene and training stage,
2. target reach rate by scene and training stage,
3. forgetting after $T_2$ and $T_3$ using reveal rate,
4. coverage count,
5. collision count,
6. training return curve.

Optional diagnostic plots:

1. decision steps per episode,
2. reveal-vs-reach gap,
3. steps to reveal,
4. steps after reveal.

## Practical acceptance criteria

A successful code deliverable should show:

- random policy logs are valid,
- Double DQN improves over random on at least $T_1$ using reveal rate, reach rate, or search efficiency,
- sequential training runs across all scenes,
- SSER or EWC variant runs without crashing,
- old-scene reveal evaluation is reported after each scene,
- saved logs and checkpoints are produced.
