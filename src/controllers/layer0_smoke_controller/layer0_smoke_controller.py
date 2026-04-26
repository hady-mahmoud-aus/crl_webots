from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from controller import Robot


WHEEL_RADIUS_M = 0.020
AXLE_LENGTH_M = 0.052
DEFAULT_WHEEL_SPEED = 3.0
POSITION_TOLERANCE_RAD = 0.05
COLLISION_THRESHOLD = 80.0
SENSOR_WARMUP_STEPS = 5

LOG_PATH = Path(__file__).with_name("artifacts") / "smoke_test_log.jsonl"


@dataclass(frozen=True)
class ActionSpec:
    name: str
    left_delta_rad: float
    right_delta_rad: float
    timeout_steps: int


def require_device(robot: Robot, name: str) -> Any:
    device = robot.getDevice(name)
    if device is None:
        raise RuntimeError(f"Missing required Webots device: {name}")
    return device


def assert_finite(name: str, values: list[float]) -> None:
    if not all(math.isfinite(value) for value in values):
        raise RuntimeError(f"{name} returned a non-finite value: {values}")


def heading_from_compass(values: list[float]) -> float:
    assert_finite("compass", values)
    return math.atan2(values[0], values[2])


class SmokeTestController:
    def __init__(self) -> None:
        self.robot = Robot()
        self.timestep = int(self.robot.getBasicTimeStep())
        self.log_path = LOG_PATH
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text("", encoding="utf-8")

        self.left_motor = require_device(self.robot, "left wheel motor")
        self.right_motor = require_device(self.robot, "right wheel motor")
        self.left_encoder = require_device(self.robot, "left wheel sensor")
        self.right_encoder = require_device(self.robot, "right wheel sensor")
        self.gps = require_device(self.robot, "gps")
        self.compass = require_device(self.robot, "compass")
        self.proximity_sensors = [
            require_device(self.robot, f"ps{index}") for index in range(8)
        ]

        self.left_encoder.enable(self.timestep)
        self.right_encoder.enable(self.timestep)
        self.gps.enable(self.timestep)
        self.compass.enable(self.timestep)
        for sensor in self.proximity_sensors:
            sensor.enable(self.timestep)

        self.left_motor.setPosition(float("inf"))
        self.right_motor.setPosition(float("inf"))
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def log_event(self, event: str, **payload: Any) -> None:
        record = {"event": event, **payload}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        print(json.dumps(record, sort_keys=True), flush=True)

    def step(self) -> None:
        if self.robot.step(self.timestep) == -1:
            raise RuntimeError("Webots simulation ended before smoke test completed.")

    def warm_up_sensors(self) -> None:
        for _ in range(SENSOR_WARMUP_STEPS):
            self.step()

    def read_proximity_values(self) -> list[float]:
        values = [float(sensor.getValue()) for sensor in self.proximity_sensors]
        assert_finite("proximity", values)
        return values

    def read_gps_values(self) -> list[float]:
        values = list(self.gps.getValues())
        assert_finite("gps", values)
        return [float(value) for value in values]

    def read_compass_values(self) -> list[float]:
        values = list(self.compass.getValues())
        assert_finite("compass", values)
        return [float(value) for value in values]

    def read_encoder_values(self) -> tuple[float, float]:
        left = float(self.left_encoder.getValue())
        right = float(self.right_encoder.getValue())
        assert_finite("wheel_encoders", [left, right])
        return left, right

    def stop_motors(self) -> None:
        self.left_motor.setVelocity(0.0)
        self.right_motor.setVelocity(0.0)

    def set_position_targets(self, left_target: float, right_target: float) -> None:
        self.left_motor.setPosition(left_target)
        self.right_motor.setPosition(right_target)
        self.left_motor.setVelocity(DEFAULT_WHEEL_SPEED)
        self.right_motor.setVelocity(DEFAULT_WHEEL_SPEED)

    def target_reached(
        self,
        current_left: float,
        current_right: float,
        left_target: float,
        right_target: float,
    ) -> bool:
        return (
            abs(current_left - left_target) <= POSITION_TOLERANCE_RAD
            and abs(current_right - right_target) <= POSITION_TOLERANCE_RAD
        )

    def run_action(self, spec: ActionSpec) -> None:
        left_start, right_start = self.read_encoder_values()
        gps_before = self.read_gps_values()
        compass_before = self.read_compass_values()
        left_target = left_start + spec.left_delta_rad
        right_target = right_start + spec.right_delta_rad
        collision = False
        collision_step = None
        max_proximity = 0.0

        self.set_position_targets(left_target, right_target)

        for step_index in range(1, spec.timeout_steps + 1):
            self.step()

            proximity_values = self.read_proximity_values()
            current_left, current_right = self.read_encoder_values()
            max_proximity = max(max_proximity, max(proximity_values))

            if max(proximity_values) >= COLLISION_THRESHOLD:
                collision = True
                collision_step = step_index
                self.stop_motors()
                break

            if self.target_reached(
                current_left,
                current_right,
                left_target,
                right_target,
            ):
                self.stop_motors()
                break

        self.step()
        gps_after = self.read_gps_values()
        compass_after = self.read_compass_values()
        left_end, right_end = self.read_encoder_values()

        self.log_event(
            "action_result",
            action=spec.name,
            collision=collision,
            collision_step=collision_step,
            collision_threshold=COLLISION_THRESHOLD,
            timeout_steps=spec.timeout_steps,
            gps_before=gps_before,
            gps_after=gps_after,
            compass_before=compass_before,
            compass_after=compass_after,
            heading_before_rad=heading_from_compass(compass_before),
            heading_after_rad=heading_from_compass(compass_after),
            left_encoder_before=left_start,
            left_encoder_after=left_end,
            right_encoder_before=right_start,
            right_encoder_after=right_end,
            left_target=left_target,
            right_target=right_target,
            max_proximity=max_proximity,
        )

    def log_device_snapshot(self) -> None:
        gps_values = self.read_gps_values()
        compass_values = self.read_compass_values()
        proximity_values = self.read_proximity_values()
        left_encoder, right_encoder = self.read_encoder_values()

        self.log_event(
            "device_snapshot",
            timestep=self.timestep,
            collision_threshold=COLLISION_THRESHOLD,
            gps=gps_values,
            compass=compass_values,
            heading_rad=heading_from_compass(compass_values),
            proximity=proximity_values,
            left_encoder=left_encoder,
            right_encoder=right_encoder,
        )

    def run(self) -> None:
        self.log_event(
            "startup",
            world_timestep=self.timestep,
            log_path=str(self.log_path),
            required_devices=[
                "left wheel motor",
                "right wheel motor",
                "left wheel sensor",
                "right wheel sensor",
                "gps",
                "compass",
                "ps0",
                "ps1",
                "ps2",
                "ps3",
                "ps4",
                "ps5",
                "ps6",
                "ps7",
            ],
        )
        self.warm_up_sensors()
        self.log_device_snapshot()

        quarter_turn_rad = (AXLE_LENGTH_M * (math.pi / 2.0)) / (2.0 * WHEEL_RADIUS_M)
        actions = [
            ActionSpec("forward", 10.0, 10.0, timeout_steps=200),
            ActionSpec(
                "rotate_left",
                -quarter_turn_rad,
                quarter_turn_rad,
                timeout_steps=120,
            ),
            ActionSpec(
                "rotate_right",
                quarter_turn_rad,
                -quarter_turn_rad,
                timeout_steps=120,
            ),
            ActionSpec("collision_probe_forward", 60.0, 60.0, timeout_steps=400),
        ]

        for spec in actions:
            self.run_action(spec)

        self.stop_motors()
        self.log_event("complete", status="awaiting_manual_webots_verification")


controller = SmokeTestController()
controller.run()

while controller.robot.step(controller.timestep) != -1:
    controller.stop_motors()
