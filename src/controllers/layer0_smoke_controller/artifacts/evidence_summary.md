# Layer 0 Evidence Summary

Status: Passed

World:
`src/worlds/test world.wbt`

Controller:
`layer0_smoke_controller`

Verification date:
2026-04-26

Evidence source:
Condensed from the prior smoke-test log run and manual Webots verification notes.

## Key checks

- Controller started without errors.
- Required devices were found: wheel motors, wheel sensors, `gps`, `compass`, and `ps0`-`ps7`.
- GPS, compass, proximity sensors, and wheel encoders returned finite values.
- Left and right rotations worked as expected with high precision.
- Early collision stopping triggered successfully on forward motion.
- Console output behavior was later fixed to mirror log events live.

## Minimal readings

- World timestep: `32`
- Collision threshold: `80.0`
- Initial heading: `3.141592653589793 rad`
- Initial GPS: `[0.0, 1.1742176720537818e-11, -4.8230609573473096e-05]`
- Initial encoder state: `left=0.0`, `right=0.0`
- Initial max proximity snapshot: `74.82776379635463`

## Action outcomes

- `forward`: collision stop triggered, `collision_step=52`, `max_proximity=80.23126250212363`
- `rotate_left`: completed without collision, final heading `1.5711106687191823 rad`
- `rotate_right`: completed without collision, final heading `-1.570764575703449 rad`

## Notes

- This summary intentionally keeps only the data needed to justify Layer 0 completion.
- Future reruns should write any working smoke-test log under `artifacts/smoke_test_log.jsonl`.
