# MEMORY.md

## Purpose

Durable project memory for agentic coding assistants.

Do not use this file for temporary logs or long experiment output.

## Agent ecosystem file layout

`AGENTS.md` stays at repository root. Supporting agent files live in `agent_docs/`.

## Project identity

Graduate RL project: continual reinforcement learning for Webots e-puck search-and-homing.

Method:

> Custom PyTorch Double DQN + selective episodic replay inspired by OPR + DQN-compatible online EWC approximation inspired by KGCRL.

This is inspired by KGCRL and OPR, not an exact implementation of either paper.

## Durable implementation decisions

- Use custom PyTorch Double DQN.
- Start with 3 actions: `forward`, `rotate_left`, `rotate_right`.
- Optional diagonal actions may be added later through an explicit action-set version.
- Use fixed-size observations per run.
- Use GPS for environment-side bookkeeping, not raw global policy input.
- Use additive rewards.
- Use selective replay before EWC if time is short.
- Use online EWC, not multi-anchor EWC.
- Use squared DQN-loss gradients as parameter importance.
- Treat moving obstacles as optional until the static pipeline works.
- Default collision detection to a proximity-threshold check using `ps0`-`ps7`.
- If proximity-based collision detection proves unreliable in manual Webots verification, a dedicated bumper/contact-style collision sensor may be added later only through explicit scope review.

## Code quality decisions

- Use functional core / imperative shell.
- Use YAML externally, then load configs into Python dataclasses.
- Require type hints on public functions/classes/dataclasses/module boundaries.
- Require tests for pure logic before expanding RL complexity.
- Use medium-small modules with clear ownership.
- Avoid monolithic scripts.
- Use minimal dependencies unless approved.
- Baseline dependencies: `torch`, `numpy`, `pandas`, `matplotlib`, `pyyaml`, `pytest`, `black`, `ruff`.
- Use minimal comments, but document Webots-specific assumptions inline.
- Prioritize clarity first; DQN updates must be batched.
- Use `black` and `ruff`.
- Use `pytest -p no:cacheprovider` by default in this repo until the local Windows pytest cache-temp permission issue is resolved.

## Manual Webots verification decision

Webots-facing milestones require manual verification.

Mock/unit tests validate pure logic only. They do not count as Webots verification.

Agents must give manual Webots instructions when user action is needed.

## Experiment integrity decision

Experiment outputs are evidence.

Agents must not fake, overwrite, cherry-pick, or delete run results unless explicitly instructed.

Each meaningful run should preserve config, timestamp, seed, metrics, notes, and checkpoint metadata.

## Evidence condensation decision

Stage-completion evidence should be stored in a highly condensed form.

Keep only the minimum data needed to support the completion claim, such as pass/fail status, key readings or metrics, relevant timestamps, and paths to preserved raw artifacts when those artifacts must exist.

Do not keep large duplicated console dumps, repeated sensor traces, or verbose scratch evidence when a short summary and a pointer to the canonical artifact are sufficient.

## Stage cleanup decision

After closing a layer, agents should remove only transient generated artifacts such as `__pycache__`, `.pyc`, `.pyo`, and disposable pytest cache folders.

Agents must not treat smoke-test logs, experiment outputs, run directories, checkpoints, replay buffers, plots, metrics, configs, or user-authored files as cleanup targets unless the user explicitly asks.

## `src/` structural cleanup decision

After a stage is completed, agents may perform conservative structural cleanup inside `src/` only if it clearly improves readability, modularity, or folder structure.

This may include renaming unclear stage-local files or folders, moving them into clearer locations, creating small supporting directories, and removing redundant leftovers.

If the cleanup touches a Webots controller name, folder, or linkage, agents must preserve valid Webots resolution, update linked references in the same change, and require manual re-verification before treating the rewired stage as stable again.

## Scope control decision

Agents must stop and ask before expanding beyond the current implementation layer.

## Path safety decision

The repo path may contain spaces, for example:

```text
C:\dev\AI Project\CRL
```

Use `pathlib`. Do not hard-code absolute paths. Do not assume paths have no spaces.

## Current repo note

Observed structure:

```text
CRL/
  papers/
  procect_docs/
  src/
```

`procect_docs/` appears to be a typo. Recommended rename: `project_docs/`.

## Safe paper wording

Use:

- "selective episodic replay inspired by OPR"
- "DQN-compatible online EWC approximation inspired by KGCRL"
- "Double DQN for discrete Webots macro-action control"

Avoid:

- "we implement KGCRL"
- "we implement OPR"
- "exact Fisher estimate from KGCRL"
