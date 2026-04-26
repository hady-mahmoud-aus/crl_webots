# IMPLEMENTATION_STATUS.md

## Purpose

Layer-by-layer implementation status.

Update after meaningful changes.

## Current status

Current layer: **Layer 0 — Environment smoke test**

Status: **Not yet verified**

Last updated: **2026-04-26**

## Evidence gate

For any completed task:

- [ ] Files changed are listed
- [ ] Automated checks are listed
- [ ] Manual Webots status is listed if applicable
- [ ] Outputs/logs are listed
- [ ] Limitations are listed

## Layer 0 — Environment smoke test

- [ ] Controller imports without error
- [ ] Devices found
- [ ] Sensors readable
- [ ] Motors controllable
- [ ] Wheel position sensors readable
- [ ] Scripted forward action works
- [ ] Scripted rotate actions work
- [ ] Collision threshold logged
- [ ] Smoke log written
- [ ] Automated checks passed
- [ ] Manual Webots verification passed

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

- [ ] `ECOSYSTEM_FEATURE_PROTOCOL.md` followed
- [ ] `AGENTS.md` updated
- [ ] `MEMORY.md` updated
- [ ] Specialized files updated
- [ ] `README_AGENT_FILES.md` updated if needed
- [ ] Follow-up tasks added to `TODO.md` if needed
