# TODO.md

## Immediate bootstrap

- [ ] Copy ecosystem files to repo root.
- [ ] Rename `procect_docs/` to `project_docs/` if safe.
- [ ] Add `.gitignore`.
- [ ] Commit or backup before agent coding.
- [ ] Confirm active Webots world and controller.

## Layer 0

- [ ] Create/verify smoke-test controller.
- [ ] Read distance sensors.
- [ ] Read GPS.
- [ ] Read Compass.
- [ ] Control wheel motors.
- [ ] Read wheel position sensors.
- [ ] Script forward/left/right actions.
- [ ] Log sensor/action results.
- [ ] Run manual Webots verification.

## Layer 1

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
