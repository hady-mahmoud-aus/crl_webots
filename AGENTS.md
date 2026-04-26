# AGENTS.md

## Location convention

This file stays at the repository root so coding agents can discover it automatically.

All supporting agent ecosystem files live in:

```text
agent_docs/
```

## Purpose

Operating instructions for any agentic coding assistant working on this repository, including Claude Code, Cursor, Copilot, ChatGPT, or similar tools.

The project goal is to implement a lightweight continual reinforcement learning pipeline for Webots e-puck search-and-homing using:

- custom PyTorch Double DQN,
- selective episodic replay inspired by OPR,
- DQN-compatible online EWC approximation inspired by KGCRL,
- sequential evaluation across three scenes.

## Read first

Before making changes, read:

1. `agent_docs/MEMORY.md`
2. `agent_docs/REPO_MAP.md`
3. `agent_docs/CODE_STYLE.md`
4. `agent_docs/PROJECT_CONTRACTS.md`
5. `agent_docs/EXPERIMENT_PROTOCOL.md`
6. `agent_docs/IMPLEMENTATION_STATUS.md`
7. `agent_docs/TODO.md`
8. `agent_docs/TEST_PLAN.md`
9. `agent_docs/MANUAL_WEBOTS_VERIFICATION.md`
10. `agent_docs/RUNBOOK.md`
11. `agent_docs/ECOSYSTEM_FEATURE_PROTOCOL.md`

Then read active project docs:

```text
project_docs/README.md
project_docs/docs/00_project_scope_and_decisions.md
project_docs/docs/04_implementation_layers.md
```

If the folder is still named `procect_docs/`, treat it as the active docs folder and recommend renaming it to `project_docs/`.

## Source of truth

Use the cleaned project docs and root ecosystem files as source of truth. The `papers/` folder is reference material only.

Do not override the project plan based on paper text unless the user asks for a research rewrite.

## Layered scope control

Work layer by layer:

1. Layer 0: Webots environment smoke test
2. Layer 1: minimal RL environment
3. Layer 2: Double DQN on one scene
4. Layer 3: sequential fine-tuning baseline
5. Layer 4: selective episodic replay
6. Layer 5: online EWC approximation
7. Layer 6: optional extensions

Do not expand scope beyond the current layer without user approval.

Scope escalation examples that require approval:

- adding Gymnasium, ROS2, PPO, DDPG, SAC, dashboards, multiprocessing, image input, curriculum learning, diagonal actions, moving-obstacle handling, or long training runs before the relevant layer is stable;
- changing observation/action dimensions;
- editing Webots world/proto/plugin files;
- adding dependencies outside the approved baseline.

## File modification rules

Allowed by default:

```text
src/controllers/**
configs/**
scripts/**
tests/**
root-level `AGENTS.md` and files under `agent_docs/`
```

Ask first before editing:

```text
src/worlds/**
src/protos/**
src/plugins/**
src/libraries/**
papers/**
project_docs/**
procect_docs/**
```

World/proto rule: solve from the controller side first. If `.wbt` or `.proto` edits appear necessary, explain why and ask for approval.

## Code quality rule

Prioritize:

> modular, functional, efficient, readable code.

Follow `agent_docs/CODE_STYLE.md`.

Use functional core / imperative shell:

- pure functions for grid, reward, observation, action math, replay ranking, DQN target math, and metrics;
- stateful code only for Webots interaction, file I/O, training orchestration, and checkpointing.

## Contract rule

Follow `agent_docs/PROJECT_CONTRACTS.md`.

Do not change observation dimensions, action IDs, reward semantics, metric names, or checkpoint compatibility without updating the relevant contract and recording the change.

Core action IDs must remain stable:

```text
0 = forward
1 = rotate_left
2 = rotate_right
```

Optional diagonal actions may be added later only through an explicit action-set version such as `five_action`.

## Testing and manual verification rule

Automated tests are required for pure logic modules.

Manual Webots verification is required for Webots-facing features. Do not mark Webots-facing tasks complete from unit tests alone.

If user action in Webots is needed, give clear instructions:

1. which world to open,
2. which controller should be assigned,
3. what to run or click,
4. what behavior to observe,
5. which log/output file to inspect,
6. what counts as pass/fail,
7. what to report if it fails.

## Evidence-based completion rule

Do not claim a task is complete unless you report:

- files changed,
- tests/checks run,
- manual Webots verification status if applicable,
- outputs/logs produced,
- remaining limitations or risks.

If something was not run, say so clearly.

## Experiment integrity rule

Never fake, cherry-pick, overwrite, or silently delete experiment results.

Every run should preserve its config, timestamp, seed, metrics, checkpoint metadata, and notes.

Do not delete runs, checkpoints, replay buffers, plots, or logs unless the user explicitly asks.

## Long-running task rule

Before starting a long training run or expensive Colab job, ask for approval and state:

- method variant,
- scenes,
- expected output files,
- approximate scope of the run,
- whether Webots/manual verification is required.

## Ecosystem feature rule

When the user asks to add a new agent ecosystem feature, follow `agent_docs/ECOSYSTEM_FEATURE_PROTOCOL.md`.

Do not add durable ecosystem rules to only one file.

## Documentation update rule

After meaningful work, update:

- `agent_docs/IMPLEMENTATION_STATUS.md`
- `agent_docs/TODO.md`
- `agent_docs/MEMORY.md` only for durable decisions
- `agent_docs/KNOWN_ISSUES.md` for bugs/workarounds

Update specialized files when contracts, commands, tests, logging, or manual verification change.

## Handoff format

End coding sessions with:

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
