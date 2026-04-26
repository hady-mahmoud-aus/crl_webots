# TODO.md

## Immediate bootstrap

- [ ] Copy ecosystem files to repo root.
- [ ] Rename `procect_docs/` to `project_docs/` if safe.
- [ ] Add `.gitignore`.
- [ ] Commit or backup before agent coding.
- [ ] Confirm active Webots world and controller.

## Layer 0

- [x] Create/verify smoke-test controller.
- [x] Read distance sensors.
- [x] Read GPS.
- [x] Read Compass.
- [x] Control wheel motors.
- [x] Read wheel position sensors.
- [x] Script forward/left/right actions.
- [x] Log sensor/action results.
- [x] Run manual Webots verification.

## Layer 1

- [ ] If Stage 0 controller/evidence structure is cleaned up, re-run manual Webots verification before relying on the renamed wiring.
- [ ] Implement environment wrapper.
- [ ] Implement observation contract.
- [ ] Implement action contract for `three_action`.
- [ ] Implement grid tracking.
- [ ] Implement reward contract.
- [ ] Implement target reveal.
- [ ] Run random policy.
- [ ] Verify reward logs.

## Layer 2

- [ ] Implement Q-network.
- [ ] Implement replay buffer.
- [ ] Implement batched Double DQN update.
- [ ] Implement checkpoint metadata.
- [ ] Run short T1 training.

## Layer 3+

- [ ] Sequential fine-tuning.
- [ ] Selective replay.
- [ ] Online EWC.
- [ ] Optional diagonal actions through `five_action` contract.
