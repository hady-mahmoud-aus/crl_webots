# 05 - Training and Evaluation

## Training protocol

Recommended full-experiment targets:

**TRAIN_EPISODES** = `2000`

**EVAL_EPISODES** = `100`

Current root schedule defaults in `schedules/helper.py` are smoke-test values:

**TRAIN_EPISODES** = `2`

**EVAL_EPISODES** = `1`

Increase these schedule constants before collecting report-quality results.

For each method variant:

1. initialize or load the model,
2. train the policy sequentially on $T_1,T_2,T_3$,
3. after each training scene, evaluate on all scenes learned so far,
4. save model checkpoints,
5. save logs and CRL artifacts when enabled.

Sequential schedule:

| Stage | Train scene | Evaluate scenes |
|---|---|---|
| 1 | $T_1$ / scene `0` | $T_1$ |
| 2 | $T_2$ / scene `1` | $T_1,T_2$ |
| 3 | $T_3$ / scene `2` | $T_1,T_2,T_3$ |

## Current controller inputs

The top-level controller uses environment variables:

| Variable | Default | Purpose |
|---|---:|---|
| `SEED` | `42` | random seed |
| `NUM_EPISODES` | `2000` | number of episodes |
| `POLICY` | `dqn` | run directory and method label |
| `SCENE_ID` | `0` | scene id: `0`, `1`, or `2` |
| `PARENT_SCENE` | `-1` | parent/previous scene label used in filenames |
| `EVAL` | `False` | evaluation mode flag |
| `PARAMS_NAME` | `None` | checkpoint filename under `runs/<POLICY>/` |
| `SELECTIVE_REPLAY_NAME` | `None` | SSER artifact filename under `runs/<POLICY>/` |
| `EWC_STATE_NAME` | `None` | EWC state filename under `runs/<POLICY>/` |

The current code resolves `PARAMS_NAME`, `SELECTIVE_REPLAY_NAME`, and `EWC_STATE_NAME` relative to `runs/<POLICY>/`.

## Method variants

Minimum variants:

1. `dqn`: Double DQN only
2. `dqn_replay`: Double DQN + SSER selective replay

Stronger variants:

3. `dqn_ewc`: Double DQN + EWC-style regularization
4. `dqn_replay_ewc`: Double DQN + SSER selective replay + EWC-style regularization

All variants should use the same action space, observation structure, target sampling rules, and reward definitions unless the experiment explicitly states otherwise.

## Root schedule scripts

The root `schedules/` directory contains executable Python schedules for Webots batch runs.

| File | Purpose |
|---|---|
| `schedules/helper.py` | Shared Webots runner, scene mapping, episode constants, model names, and cleanup logic |
| `schedules/dqn_schedule.py` | Full `dqn` baseline schedule: sequential training/evaluation plus scratch scene 1 and scene 2 baselines |
| `schedules/dqn_replay_schedule.py` | `dqn_replay` schedule with SSER collection and replay-dependent training |
| `schedules/dqn_ewc_schedule.py` | `dqn_ewc` schedule with EWC state loading/saving |
| `schedules/dqn_replay_ewc_schedule.py` | Combined SSER + EWC schedule |
| `schedules/dqn_missing_schedule.py` | One-job helper schedule for evaluating the scratch scene 2 `dqn` checkpoint |

Run schedules from the repository root, for example:

```powershell
python schedules\dqn_schedule.py
python schedules\dqn_replay_schedule.py
python schedules\dqn_ewc_schedule.py
python schedules\dqn_replay_ewc_schedule.py
python schedules\dqn_missing_schedule.py
```

The helper expects the `webots` command to be available on `PATH`.

## Schedule execution flow

For each job, `schedules/helper.py`:

1. maps `SCENE_ID` to a Webots world,
2. copies the current process environment,
3. overlays the job dictionary as environment variables,
4. launches Webots in batch mode,
5. waits for the controller process to complete,
6. kills remaining Webots processes,
7. raises an error if the Webots process exits with a nonzero code.

Scene mapping:

| `SCENE_ID` | Task | World file |
|---:|---|---|
| `0` | $T_1$: empty room | `src/worlds/scene_1_empty.wbt` |
| `1` | $T_2$: static obstacles | `src/worlds/scene_2_obstacles.wbt` |
| `2` | $T_3$: dynamic or harder obstacle scene | `src/worlds/scene_3_dynamic.wbt` |

Webots is launched with:

```text
webots --batch --mode=fast --no-rendering --stdout --stderr <world_path>
```

Cleanup behavior:

- On Windows, the helper calls `taskkill` for `webots-bin.exe` and `webots.exe`.
- On non-Windows systems, it calls `pkill -f webots-bin` and `pkill -f webots`.
- It waits three seconds after cleanup before the next job.

## Schedule artifact dependencies

Common model filenames from `MODEL_NAMES`:

| Label | Filename | Meaning |
|---|---|---|
| `MODEL_0` | `model-_-0.pt` | model trained from scratch on scene 0 |
| `MODEL_01` | `model-0-1.pt` | model trained on scene 1 from scene 0 parent |
| `MODEL_12` | `model-1-2.pt` | model trained on scene 2 from scene 1 parent |
| `MODEL_1` | `model-_-1.pt` | model trained from scratch on scene 1 |
| `MODEL_2` | `model-_-2.pt` | model trained from scratch on scene 2 |

SSER artifact dependencies:

| Artifact | Produced by | Used by |
|---|---|---|
| `selective-replay-buffer-0.pt` | scene 0 SSER collection/eval run | scene 1 replay training |
| `selective-replay-buffer-0-1.pt` | scene 1 SSER collection/eval run | scene 2 replay training/evaluation jobs that need old memory |

EWC artifact dependencies:

| Artifact | Produced by | Used by |
|---|---|---|
| `ewc_state-0.pt` | scene 0 EWC training | scene 1 EWC training |
| `ewc_state-0-1.pt` | scene 1 EWC training | scene 2 EWC training and EWC evaluation jobs |

Current implementation notes:

- SSER episode memory is collected during evaluation-style collection runs because replay writing is enabled in eval mode for replay policies.
- EWC state is saved after EWC training runs from the reservoir of transitions collected during training.
- Current SSER stores only episodes with `reached=True`; reveal-only episodes are not currently saved even though reveal rate is the primary metric.
- Current PyTorch versions default to restricted `torch.load` behavior; loading saved replay objects may require code support for non-weights-only artifact loading.

## Current output files

Outputs are written under:

```text
runs/<POLICY>/
```

Current controller filename patterns:

| Output | Pattern |
|---|---|
| logs | `logs-<train_or_eval>-<parent>-<scene>.csv` |
| model checkpoint | `model-<parent>-<scene>.pt` |
| SSER memory | `selective-replay-buffer-0.pt` or `selective-replay-buffer-0-1.pt` |
| EWC state | `ewc_state-0.pt` or `ewc_state-0-1.pt` |

When `PARENT_SCENE=-1`, the filename parent label is `_`.

## Evaluation seeds

Use fixed evaluation seeds for each scene when collecting final results. This makes training-stage comparisons more reliable.

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
| `timeout` | max decision-step limit reached before target reach |
| `unique_cells_covered` | visited-cell count |
| `reward` | total episode reward |
| `collisions` | collision count |
| `decision_steps` | number of DQN macro-actions |

Recommended future logging cleanup:

- split timeout into separate pre-reveal and post-reveal timeout fields,
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
- Double DQN improves over random on at least $T_1$ using reveal rate, target reach rate, coverage, return, or search efficiency,
- sequential training runs across all scenes,
- SSER or EWC variant runs without crashing,
- old-scene reveal evaluation is reported after each scene,
- saved logs, checkpoints, and enabled CRL artifacts are produced.
