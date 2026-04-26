# EXPERIMENT_PROTOCOL.md

## Purpose

Config, logging, reproducibility, and experiment integrity rules.

## Config-first rule

Training parameters, reward values, scene IDs, action settings, replay settings, EWC settings, and output paths should come from YAML configs loaded into dataclasses.

Do not hard-code experiment settings inside training scripts unless they are true constants.

## Recommended configs

```text
configs/
  layer0_smoke.yaml
  layer1_random.yaml
  dqn_base.yaml
  replay.yaml
  ewc.yaml
  replay_ewc.yaml
```

## Minimum config fields

```yaml
project:
  seed: 0
  output_dir: runs

env:
  max_decision_steps: 200
  cell_size_m: 0.2
  reveal_radius_m: 0.4
  goal_radius_m: 0.1
  cell_lock_steps: 2

actions:
  action_set: three_action
  forward_distance_m: 0.2
  turn_angle_deg: 90
  macro_timeout_steps: 100
  stop_on_collision: true

dqn:
  hidden_sizes: [128, 128]
  gamma: 0.99
  learning_rate: 0.0005
  batch_size: 64
  replay_capacity: 50000
  target_update_interval: 1000

selective_replay:
  enabled: false
  top_k_per_scene: 10
  old_replay_fraction: 0.2

ewc:
  enabled: false
  lambda: 10.0
  rho: 0.9
  importance_batches: 20
```

## Experiment integrity

Never fake, cherry-pick, overwrite, or silently delete results.

Each run should get a unique timestamped directory.

Do not reuse a run directory unless explicitly resuming and documenting it.

## Run directory

```text
runs/
  run_YYYYMMDD_HHMMSS/
    config.yaml
    notes.md
    checkpoints/
    metrics/
    replay/
    plots/
```

## Required run metadata

Capture when possible:

- timestamp,
- config path and full resolved config,
- random seed,
- method variant,
- scene/world file,
- observation version and dimension,
- action-set version and dimension,
- git commit/hash if available,
- dependency versions if easy,
- Webots version if easy,
- whether run was manual/headless.

## Logs

Recommended CSVs:

```text
metrics/train_log.csv
metrics/eval_log.csv
metrics/forgetting.csv
metrics/episode_metrics.csv
```

Stable metric names are defined in `PROJECT_CONTRACTS.md`.

## Reproducibility checklist

Before presenting a result, confirm:

- [ ] config saved,
- [ ] seed saved,
- [ ] run directory preserved,
- [ ] checkpoint metadata saved,
- [ ] evaluation scenes recorded,
- [ ] observation/action versions recorded,
- [ ] manual Webots verification status recorded if relevant.

## Generated file hygiene

Do not commit large generated artifacts unless asked:

- checkpoints,
- replay buffers,
- videos,
- run logs,
- generated plots,
- large CSVs.

Use `.gitignore` for generated outputs.

## Long-running runs

Before starting long training, ask for approval and state:

- variant,
- scenes,
- number of episodes/steps,
- expected outputs,
- whether local Webots or Colab is involved.
