# REPO_MAP.md

## Purpose

Repository layout, editable areas, and path rules.

## Agent file layout

```text
CRL/
  AGENTS.md
  agent_docs/
    *.md
```

Keep `AGENTS.md` at repo root for discoverability. Keep supporting files in `agent_docs/` for cleanliness.

## Current observed layout

```text
CRL/
  papers/
    kgcrl_paper.md
    optimal_policy_replay.md

  procect_docs/
    README.md
    docs/

  src/
    .vscode/
    controllers/
      layer0_smoke_controller/
    libraries/
    plugins/
    protos/
    worlds/
      test world.wbt
```

Recommended rename:

```text
procect_docs/ -> project_docs/
```

Until renamed, treat `procect_docs/` as the active docs folder.

## Editable areas

Allowed by default:

```text
src/controllers/**
configs/**
scripts/**
tests/**
root-level ecosystem markdown files
```

Ask before editing:

```text
src/worlds/**
src/protos/**
src/plugins/**
src/libraries/**
papers/**
project_docs/**
procect_docs/**
```

## Post-stage `src/` cleanup

After a stage is completed, agents may clean up `src/` structure only when needed to improve readability or modularity.

Typical allowed changes:

- rename unclear controller-side files or folders,
- move kept artifacts into clearer stage-local locations,
- add small directories such as `artifacts/` when they immediately hold real files,
- remove empty or redundant leftovers.

Webots safety constraints:

- preserve valid controller lookup from world files,
- avoid renaming or moving world/proto/plugin assets unless required to keep runtime wiring valid,
- if a controller rename forces a world reference update, treat that as a coupled change and require manual Webots re-verification.

## Recommended code layout

```text
src/controllers/crl_controller/
  crl_controller.py
  config.py

  env/
    webots_env.py
    sensors.py
    actions.py
    grid.py
    rewards.py
    observations.py

  rl/
    dqn.py
    replay_buffer.py
    selective_memory.py
    ewc.py
    trainer.py
    evaluator.py

  utils/
    seeding.py
    paths.py
    logging_utils.py
    metrics.py
```

## Recommended support layout

```text
configs/
  layer0_smoke.yaml
  layer1_random.yaml
  dqn_base.yaml
  replay.yaml
  ewc.yaml
  replay_ewc.yaml

scripts/
  run_smoke_test.py
  run_random_policy.py
  train.py
  train_sequential.py
  evaluate.py
  plot_metrics.py

tests/
  test_grid.py
  test_rewards.py
  test_observations.py
  test_actions.py
  test_replay_buffer.py
  test_selective_memory.py
  test_dqn_targets.py
  test_ewc.py

runs/
  .gitkeep
```

## Windows/path safety

Use `pathlib`.

Do not hard-code absolute paths.

Do not assume paths lack spaces.

Be careful with Webots controllers, which may execute from the controller directory rather than the repo root.

If a post-stage cleanup renames a controller folder, update the linked world controller reference in the same change and re-verify manually in Webots.
