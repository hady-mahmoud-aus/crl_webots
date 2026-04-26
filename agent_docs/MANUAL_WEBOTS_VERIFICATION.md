# MANUAL_WEBOTS_VERIFICATION.md

## Purpose

Manual verification requirements for Webots-facing work.

Automated unit tests are necessary but not sufficient for simulator interaction.

## Rule

Manual Webots verification is required for changes touching:

- device names,
- sensors,
- motors,
- wheel position sensors,
- controller stepping,
- world reset behavior,
- GPS,
- Compass,
- collision detection,
- target/scene assumptions,
- macro-action execution,
- live controller logging.

## Agent instruction format

When manual verification is needed, agents must provide:

```md
## Manual Webots check needed

### Goal
...

### Steps
1. Open Webots.
2. Open `src/worlds/<world>.wbt`.
3. Confirm controller `<controller_name>`.
4. Press Run / Step.
5. Observe ...
6. Check log ...

### Expected result
- ...

### If it fails, report
- Webots console error,
- whether robot moved,
- sensor/log values,
- screenshot if useful.
```

## Layer 0 checklist

- [ ] World opens without errors.
- [ ] Correct controller is assigned.
- [ ] Controller starts without errors.
- [ ] Robot is visible.
- [ ] Distance sensors produce values.
- [ ] GPS position is finite and changes with motion.
- [ ] Compass heading is finite and changes with rotation.
- [ ] Wheel motors accept commands.
- [ ] Wheel position sensors change.
- [ ] Forward action moves approximately forward.
- [ ] Rotate-left and rotate-right rotate in opposite directions.
- [ ] Collision threshold triggers near obstacles.
- [ ] Smoke-test log is written.

## Layer 1 checklist

- [ ] `reset()` starts a valid episode.
- [ ] `step(action)` executes each core action.
- [ ] Observation vector has fixed size.
- [ ] Target features are zero before reveal.
- [ ] Target features become valid after reveal.
- [ ] Grid cell changes with movement.
- [ ] Reward component logs make sense.
- [ ] Episode terminates correctly.
- [ ] Random policy logs are written.

## Action-change checklist

Required after adding diagonal or modified macro-actions:

- [ ] Action IDs match `PROJECT_CONTRACTS.md`.
- [ ] Forward still works.
- [ ] Rotate-left/right still work.
- [ ] New actions move in expected direction.
- [ ] Timeout works.
- [ ] Collision interruption works.
- [ ] Logs include action ID/name/duration/collision status.
