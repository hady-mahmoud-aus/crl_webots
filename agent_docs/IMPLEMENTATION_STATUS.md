# IMPLEMENTATION_STATUS.md

## Purpose

Layer-by-layer implementation status.

Update after meaningful changes.

## Current status

Current layer: **Layer 1 — Minimal RL environment**

Status: **Layer 0 closed; Layer 1 not started**

Last updated: **2026-04-26**

Note: Layer 0 was closed after controller-side smoke testing, condensed evidence capture, and manual Webots verification of motion and collision stopping. Stage 0 assets are now being structurally cleaned up under `src/controllers/layer0_smoke_controller/`; because that cleanup changes Webots-facing controller linkage, manual re-verification is required before relying on the renamed wiring. `ruff` could not be run in the current environment because it is not installed.

## Evidence gate

For any completed task:

- [ ] Files changed are listed
- [ ] Automated checks are listed
- [ ] Manual Webots status is listed if applicable
- [ ] Outputs/logs are listed
- [ ] Limitations are listed

## Layer 0 — Environment smoke test

- [x] Controller imports without error
- [x] Devices found
- [x] Sensors readable
- [x] Motors controllable
- [x] Wheel position sensors readable
- [x] Scripted forward action works
- [x] Scripted rotate actions work
- [x] Collision threshold logged
- [x] Smoke log written
- [x] Automated checks passed
- [x] Manual Webots verification passed

## Layer 1 — Minimal RL environment

- [ ] `reset()` implemented
- [ ] `step(action)` implemented
- [ ] Observation contract implemented
- [ ] Core three-action set implemented
- [ ] GPS grid tracking implemented
- [ ] Target reveal implemented
- [ ] Reward contract implemented
- [ ] Random policy runs
- [ ] Automated checks passed
- [ ] Manual Webots verification passed

## Layer 2 — Double DQN baseline

- [ ] Q-network implemented
- [ ] Replay buffer implemented
- [ ] Double DQN target implemented
- [ ] Batched update implemented
- [ ] Checkpoint save/load implemented
- [ ] Short training run completed
- [ ] Policy improves on T1 or limitation documented

## Layer 3 — Sequential fine-tuning baseline

- [ ] Train/eval schedule implemented
- [ ] T1 -> evaluate T1
- [ ] T2 -> evaluate T1,T2
- [ ] T3 -> evaluate T1,T2,T3
- [ ] Forgetting metrics saved

## Layer 4 — Selective episodic replay

- [ ] Episode recording implemented
- [ ] Top-K ranking implemented
- [ ] Selective memory save/load implemented
- [ ] Mixed replay implemented
- [ ] Replay variant compared with fine-tuning

## Layer 5 — Online EWC approximation

- [ ] Parameter anchor saved
- [ ] Squared-gradient importance implemented
- [ ] Online accumulator implemented
- [ ] EWC loss implemented
- [ ] EWC variants run without instability

## Ecosystem feature maintenance

When adding ecosystem features:

- [x] `ECOSYSTEM_FEATURE_PROTOCOL.md` followed
- [x] `AGENTS.md` updated
- [x] `MEMORY.md` updated
- [x] Specialized files updated
- [x] `README_AGENT_FILES.md` updated if needed
- [x] Follow-up tasks added to `TODO.md` if needed
