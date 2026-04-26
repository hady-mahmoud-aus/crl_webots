# RUNBOOK.md

## Purpose

Practical workflows, commands, debugging order, and handoff format.

## Basic setup

Install baseline dependencies:

```powershell
pip install torch numpy pandas matplotlib pyyaml pytest black ruff
```

Run code quality checks:

```powershell
black .
ruff check .
pytest -p no:cacheprovider
```

## Manual Webots workflow

When asked to verify in Webots:

1. Open Webots.
2. Open the relevant world, usually:

```text
src/worlds/test world.wbt
```

3. Confirm the expected controller is assigned.
4. Run or step the simulation as instructed.
5. Observe behavior.
6. Check Webots console errors.
7. Check requested logs.
8. Report pass/fail and requested details.

Agents must provide task-specific manual instructions.

## Layer 0 smoke test

Goal: verify devices, sensors, motors, scripted motion, and logging.

Expected future command:

```powershell
python .\scripts\run_smoke_test.py
```

If Webots must launch the controller manually, follow agent instructions and record the result.

## Pytest cache workaround

This repository currently uses:

```powershell
pytest -p no:cacheprovider
```

because local Windows pytest cache-temp directory creation can fail with access-denied errors unrelated to project code.

`pytest.ini` also excludes `pytest-cache-files-*` and `.pytest_cache` from recursion so leftover temp folders are not collected as tests.

## Layer 1 random policy

Expected future command:

```powershell
python .\scripts\run_random_policy.py --config .\configs\layer1_random.yaml
```

## Training

Base DQN:

```powershell
python .\scripts\train_sequential.py --config .\configs\dqn_base.yaml --variant finetune
```

Replay:

```powershell
python .\scripts\train_sequential.py --config .\configs\replay.yaml --variant replay
```

EWC:

```powershell
python .\scripts\train_sequential.py --config .\configs\ewc.yaml --variant ewc
```

Replay + EWC:

```powershell
python .\scripts\train_sequential.py --config .\configs\replay_ewc.yaml --variant replay_ewc
```

Only use these after earlier layers are verified.

## Debugging escalation ladder

When something fails, debug in this order:

1. imports,
2. config loading,
3. path handling,
4. Webots device names,
5. sensor values,
6. manual scripted actions,
7. random policy,
8. reward component logs,
9. observation/action contracts,
10. replay buffer,
11. DQN loss,
12. training stability.

Do not jump to RL hyperparameters before environment checks pass.

## Adding an ecosystem feature

Follow `ECOSYSTEM_FEATURE_PROTOCOL.md`.

Do not put durable rules in only one file.

## Stage-completion cleanup

After a layer is closed, remove only transient generated artifacts that are no longer needed, for example:

- `__pycache__/`
- `*.pyc`
- `*.pyo`
- disposable pytest cache folders
- local scratch debug files created only for short-lived validation

Do not delete evidence needed for handoff or completion claims, including smoke-test logs, run outputs, metrics, checkpoints, replay buffers, plots, or user-authored notes.

If a file may be useful for the next layer or for reproducing the completed stage, keep it and mention it in the handoff.

## Stage evidence style

When keeping evidence from a completed stage:

- prefer a short summary over raw log dumps,
- keep only the smallest set of readings or metrics needed to support pass/fail,
- include paths to canonical artifacts instead of copying their contents into multiple files,
- keep extra detail only when it is needed to explain a failure, instability, or unresolved risk.

## `src/` structural cleanup after stage completion

When a completed stage leaves awkward names or clutter inside `src/`, agents may do a conservative structural cleanup if it improves readability or modularity.

Allowed examples:

- rename a stage-local controller folder or file,
- move evidence into an `artifacts/` subdirectory,
- remove empty folders left behind.

Webots-specific caution:

- preserve the expected Webots controller directory structure,
- if a controller rename changes world/controller linkage, update the linked world reference in the same change,
- re-run manual Webots verification before considering the rewired stage stable.
- for Stage 0, prefer keeping the world filename unchanged and only updating the controller assignment when the controller folder is renamed.

## Handoff format

```md
## Handoff

Changed:
- ...

Verified:
- ...

Manual Webots check:
- Needed / Passed / Not run

Outputs:
- ...

Current layer:
- ...

Known issues:
- ...

Next recommended task:
- ...
```
