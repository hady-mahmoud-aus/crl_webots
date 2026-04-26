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
pytest
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
